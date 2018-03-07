import re
ACCENT_TEENCODE_REG = re.compile(ur"[\'\^\?\~\*\`]")
sen = "To^j dda^u co' lo^~j gj` co* chu* ' "
sen2 = ACCENT_TEENCODE_REG.sub("",sen)
print sen2