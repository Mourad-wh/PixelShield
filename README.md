# PixelShield: Enhanced Image Encryption

Following the brute-force vulnerability discovered in the original PixelSwapping project, PixelShield was developed as a robust solution to counter this weakness. This script introduces a more secure encryption approach by:

- Generating an initial key derived from the image’s own hash using SHA-512.

- Creating derivative keys from this hash to apply multiple layers of encryption.

This layered encryption strategy significantly strengthens the image’s defense, making brute-force attacks far more difficult and impractical.
