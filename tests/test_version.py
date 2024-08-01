"""version test"""

import pytest

from fake_sensor.protocol.field_version import Version


def test_version_initialization():
    version = Version(1, 2, 3, 0x1ABCDEF0)
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert version.git_sha == 0x1ABCDEF0


def test_version_repr():
    version = Version(1, 2, 3, 0x1ABCDEF0)
    assert repr(version) == "Version(major=1, minor=2, patch=3, git_sha=1abcdef0)"


def test_version_str():
    version = Version(1, 2, 3, 0x1ABCDEF0)
    assert str(version) == "1.2.3-g1abcdef0"


def test_version_to_bytes():
    version = Version(1, 2, 3, 0x1ABCDEF0)
    assert version.to_bytes() == b"\x01\x02\x03\x1a\xbc\xde\xf0"


def test_version_from_bytes():
    data = b"\x01\x02\x03\x1a\xbc\xde\xf0"
    version = Version.from_bytes(data)
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert version.git_sha == 0x1ABCDEF0


def test_invalid_major_minor_patch():
    with pytest.raises(ValueError):
        Version(256, 0, 0, 0x1ABCDEF0)
    with pytest.raises(ValueError):
        Version(0, 256, 0, 0x1ABCDEF0)
    with pytest.raises(ValueError):
        Version(0, 0, 256, 0x1ABCDEF0)


def test_invalid_git_sha():
    with pytest.raises(ValueError):
        Version(1, 2, 3, 0x100000000)


def test_invalid_from_bytes():
    with pytest.raises(ValueError):
        Version.from_bytes(b"\x01\x02\x03\x1a\xbc\xde")  # Less than 7 bytes
    with pytest.raises(ValueError):
        Version.from_bytes(b"\x01\x02\x03\x1a\xbc\xde\xf0\x01")  # More than 7 bytes
