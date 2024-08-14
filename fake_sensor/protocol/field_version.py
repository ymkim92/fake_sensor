"""version field"""


class Version:
    # pylint: disable=fixme
    # TODO add commit count
    # https://py-pkgs.org/07-releasing-versioning#automatic-version-bumping

    def __init__(self, major: int, minor: int, patch: int, git_sha: int):
        if not (0 <= major < 256 and 0 <= minor < 256 and 0 <= patch < 256):
            raise ValueError("Major, minor, and patch must be in the range 0-255.")
        if not 0 <= git_sha <= 0xFFFFFFFF:
            raise ValueError("git_sha must be exactly 4 bytes.")

        self.major = major
        self.minor = minor
        self.patch = patch
        self.git_sha = git_sha

    def __repr__(self) -> str:
        output = f"Version(major={self.major}, minor={self.minor}, patch={self.patch}, "
        output += f"git_sha={self.git_sha:08x})"
        return output

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}-g{self.git_sha:08x}"

    def to_bytes(self) -> bytes:
        return bytes([self.major, self.minor, self.patch]) + self.git_sha.to_bytes(4, "big")

    @classmethod
    def from_bytes(cls, data: bytes) -> "Version":
        if len(data) != 7:
            raise ValueError("Data must be exactly 7 bytes.")
        major, minor, patch = data[:3]
        git_sha = int.from_bytes(data[3:], "big")
        return cls(major, minor, patch, git_sha)
