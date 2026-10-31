import math

# Generate a high-fidelity, anatomically proportioned head silhouette path (profile facing right)
# Viewbox: 0 0 300 260
# Key reference points:
# Back of neck: (70, 245) -> curves up to occiput (65, 175) -> skull crown (110, 40)
# Forehead: (170, 48) -> brow: (195, 90) -> nasion (indent): (192, 98)
# Nose bridge: (200, 110) -> nose tip: (218, 122) -> subnasale (base): (198, 128)
# Philtrum: (200, 134) -> upper lip: (208, 138) -> mouth corner/crease: (199, 143)
# Lower lip: (206, 149) -> labiomental groove (chin indent): (198, 156)
# Mental protuberance (chin tip): (207, 168) -> chin curve: (202, 178)
# Jawline: (185, 192) -> angle of mandible: (155, 198)
# Front of neck / throat: (160, 215) -> clavicular base: (175, 245)

profile_path = (
    "M 70 245 "
    "C 68 215, 64 190, 65 170 "
    "C 66 130, 75 75, 115 45 "
    "C 135 30, 160 32, 175 48 "
    "C 188 60, 193 78, 195 90 "
    "C 193 96, 191 98, 192 101 "
    "C 196 106, 210 115, 218 122 "
    "C 214 126, 202 127, 198 129 "
    "C 199 132, 205 135, 208 138 "
    "C 205 141, 198 142, 199 144 "
    "C 202 147, 205 149, 206 150 "
    "C 203 153, 198 154, 198 157 "
    "C 202 162, 207 166, 207 170 "
    "C 204 176, 195 182, 185 190 "
    "C 172 198, 160 205, 160 220 "
    "C 160 230, 166 238, 175 245 "
    "Z"
)

print("Generated profile path. Length:", len(profile_path))
