# Security

## Check what you installed

Nexora is shared as an APK, so check it before you install.

1. Compare the file's SHA-256 with the one in the [README](README.md#download).
2. Check the signing certificate with `apksigner verify --print-certs nexora.apk`. Every Nexora APK is signed with the same key; its SHA-256 digest is:

```
403c5218eeddc9f23d628502a542ef60665af62ae33e3d66d5a7df82a3551028
```

A copy of Nexora with a different certificate is not from this project. Only download from [this repository's releases](https://github.com/Crylord-zx/NEXORA/releases) or <https://nexora-apk.vercel.app>.

## Report a problem

If you find a security problem, [open an issue](https://github.com/Crylord-zx/NEXORA/issues/new) and describe what you saw, without posting steps that would let others abuse it. Include the app version (Profile, then Version).
