# Deploying OrangeLion on Docker, Kubernetes, and OpenShift

OrangeLion is a standard Guacamole CSS extension (`.jar`). Guacamole loads every
jar it finds in `GUACAMOLE_HOME/extensions/`. The official `guacamole/guacamole`
image treats the `GUACAMOLE_HOME` environment variable as a **template
directory** that it copies into the live home on startup, next to the
auto-installed auth extensions (LDAP, database, and so on).

So on every platform the task is the same:

1. Place `guacamole-theme-orangelion.jar` at `<template>/extensions/guacamole-theme-orangelion.jar`.
2. Set `GUACAMOLE_HOME` to `<template>`.
3. Restart, then hard refresh the browser.

Success looks the same everywhere, in the container logs:

```
Extension "OrangeLion Theme" (orangelion) loaded
```

The prebuilt jar is attached to every [release](https://github.com/rupivbluegreen/orangelion-theme/releases). A stable "latest" URL is available:

```
https://github.com/rupivbluegreen/orangelion-theme/releases/latest/download/guacamole-theme-orangelion.jar
https://github.com/rupivbluegreen/orangelion-theme/releases/latest/download/guacamole-theme-orangelion.jar.sha256
```

---

## 1. Docker and Docker Compose

Mount a folder that contains `extensions/guacamole-theme-orangelion.jar` and point `GUACAMOLE_HOME` at it.

```yaml
services:
  guacamole:
    image: guacamole/guacamole:1.6.0
    environment:
      GUACAMOLE_HOME: /guac-home
      GUACD_HOSTNAME: guacd
      # ... your database and auth variables ...
    volumes:
      - ./guac-home:/guac-home:ro   # ./guac-home/extensions/guacamole-theme-orangelion.jar
    ports:
      - "8080:8080"
```

Plain `docker run` works the same way with a bind mount:

```bash
mkdir -p guac-home/extensions
curl -fsSL -o guac-home/extensions/guacamole-theme-orangelion.jar \
  https://github.com/rupivbluegreen/orangelion-theme/releases/latest/download/guacamole-theme-orangelion.jar
docker run -d -p 8080:8080 \
  -e GUACAMOLE_HOME=/guac-home -e GUACD_HOSTNAME=guacd \
  -v "$PWD/guac-home:/guac-home:ro" guacamole/guacamole:1.6.0
```

See [INSTRUCTIONS.md](../INSTRUCTIONS.md) for the full walkthrough.

---

## 2. Kubernetes

### Recommended: an initContainer that pulls the release

An `initContainer` downloads the signed release jar (and verifies its checksum)
into a shared `emptyDir` that the main container uses as the `GUACAMOLE_HOME`
template. This tracks the published release and keeps no jar in your image.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: guacamole
spec:
  replicas: 1
  selector:
    matchLabels: { app: guacamole }
  template:
    metadata:
      labels: { app: guacamole }
    spec:
      volumes:
        - name: guac-home
          emptyDir: {}
      initContainers:
        - name: fetch-orangelion
          image: curlimages/curl:8.10.1
          command: ["/bin/sh", "-c"]
          args:
            - |
              set -eu
              mkdir -p /guac-home/extensions
              base=https://github.com/rupivbluegreen/orangelion-theme/releases/latest/download
              curl -fsSL "$base/guacamole-theme-orangelion.jar"        -o /guac-home/extensions/guacamole-theme-orangelion.jar
              curl -fsSL "$base/guacamole-theme-orangelion.jar.sha256" -o /tmp/orangelion.sha256
              cd /guac-home/extensions && sed "s| .*|  guacamole-theme-orangelion.jar|" /tmp/orangelion.sha256 | sha256sum -c -
          volumeMounts:
            - name: guac-home
              mountPath: /guac-home
      containers:
        - name: guacamole
          image: guacamole/guacamole:1.6.0
          env:
            - { name: GUACAMOLE_HOME, value: /guac-home }
            - { name: GUACD_HOSTNAME, value: guacd }
            # ... your database and auth env vars ...
          ports:
            - containerPort: 8080
          volumeMounts:
            - name: guac-home
              mountPath: /guac-home
```

### Alternative: a ConfigMap holding the jar

The jar is only a few kilobytes, well under the 1 MB ConfigMap limit. Create the
ConfigMap from the downloaded jar, then mount it read only into the template. The
image copies out of the template, so a read-only mount is fine.

```bash
curl -fsSL -o guacamole-theme-orangelion.jar \
  https://github.com/rupivbluegreen/orangelion-theme/releases/latest/download/guacamole-theme-orangelion.jar
kubectl create configmap orangelion-theme \
  --from-file=guacamole-theme-orangelion.jar=guacamole-theme-orangelion.jar
```

```yaml
      volumes:
        - name: guac-home
          emptyDir: {}
        - name: orangelion
          configMap:
            name: orangelion-theme
      # initContainer copies the jar into the writable template:
      initContainers:
        - name: place-orangelion
          image: busybox:1.37
          command: ["sh", "-c", "mkdir -p /guac-home/extensions && cp /cm/guacamole-theme-orangelion.jar /guac-home/extensions/"]
          volumeMounts:
            - { name: guac-home, mountPath: /guac-home }
            - { name: orangelion, mountPath: /cm, readOnly: true }
```

The main container is identical to the recommended example above (mount
`guac-home`, set `GUACAMOLE_HOME=/guac-home`).

---

## 3. OpenShift

The manifests above work on OpenShift with one important adjustment for the
**restricted SCC**, which runs pods as a random, non-root UID.

### The gotcha: a writable HOME

The image writes its live home to `$HOME/.guacamole`. Under a random UID there is
usually no matching entry in `/etc/passwd`, so `$HOME` resolves to `/`, which the
random UID cannot write. Startup then fails while creating the home directory.

Fix it by giving the pod a writable `HOME` on an `emptyDir`. Do **not** hardcode
`runAsUser`; let OpenShift assign the UID.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: guacamole
spec:
  replicas: 1
  selector:
    matchLabels: { app: guacamole }
  template:
    metadata:
      labels: { app: guacamole }
    spec:
      volumes:
        - { name: guac-home, emptyDir: {} }   # GUACAMOLE_HOME template
        - { name: home,      emptyDir: {} }    # writable HOME for the random UID
      initContainers:
        - name: fetch-orangelion
          image: curlimages/curl:8.10.1
          command: ["/bin/sh", "-c"]
          args:
            - |
              set -eu
              mkdir -p /guac-home/extensions
              base=https://github.com/rupivbluegreen/orangelion-theme/releases/latest/download
              curl -fsSL "$base/guacamole-theme-orangelion.jar" -o /guac-home/extensions/guacamole-theme-orangelion.jar
          volumeMounts:
            - { name: guac-home, mountPath: /guac-home }
      containers:
        - name: guacamole
          image: guacamole/guacamole:1.6.0
          env:
            - { name: HOME,           value: /home/guacamole }   # the key fix
            - { name: GUACAMOLE_HOME, value: /guac-home }
            - { name: GUACD_HOSTNAME, value: guacd }
            # ... your database and auth env vars ...
          ports:
            - containerPort: 8080
          volumeMounts:
            - { name: guac-home, mountPath: /guac-home }
            - { name: home,      mountPath: /home/guacamole }
```

Deploy and expose it:

```bash
oc apply -f guacamole-deployment.yaml
oc expose deploy/guacamole --port=8080
oc expose svc/guacamole          # creates an external Route
```

### Alternative: bake the jar into an image (BuildConfig or ImageStream)

If your policy forbids pulling from the internet at runtime, build a small
derived image and let OpenShift host it:

```Dockerfile
FROM guacamole/guacamole:1.6.0
COPY guacamole-theme-orangelion.jar /guac-home/extensions/guacamole-theme-orangelion.jar
ENV GUACAMOLE_HOME=/guac-home
```

```bash
oc new-build --name orangelion-guacamole --binary --strategy=docker
oc start-build orangelion-guacamole --from-dir=. --follow
oc new-app orangelion-guacamole
```

The `HOME` note above still applies to the derived image.

> Note: OpenShift SCC configuration varies between clusters. Treat these
> manifests as a working starting point and adapt security contexts, storage,
> and networking to your environment. If your cluster pins the image to its
> built-in UID (1000) rather than a random one, the `HOME` fix is not needed.

---

## Verify (any platform)

1. Check the logs: `... | grep OrangeLion` should show
   `Extension "OrangeLion Theme" (orangelion) loaded`.
2. Open the portal and hard refresh (Ctrl+Shift+R). The login is orange, the tab
   shows the lion favicon.
3. If colours do not change, the browser cached the old CSS. Hard refresh again,
   or restart the pod so a fresh aggregated stylesheet is served.
