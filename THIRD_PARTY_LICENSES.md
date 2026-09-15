# Third-Party Licenses

## Ghostscript

The bundled Windows executable (built with PyInstaller) includes an
unmodified copy of Ghostscript's Windows binaries (`gswin64c.exe`,
`gsdll64.dll`, and the supporting `lib`/`Resource` files), stored in
`vendor/gs/` at build time and embedded into the `.exe`.

Ghostscript is licensed under the **GNU Affero General Public License
v3.0 (AGPL-3.0)**. A full copy of the license text is placed alongside
the bundled binary at `vendor/gs/LICENSE`, and is also permanently
available at <https://www.gnu.org/licenses/agpl-3.0.txt>.

This project's own source code (`engine/`, `gui.py`, `main.py`) invokes
Ghostscript as a separate, unmodified external program via Python's
`subprocess` module. It does not link against, embed, or modify
Ghostscript's source code.

Ghostscript's own source code is publicly available at:
- <https://www.ghostscript.com/>
- <https://git.ghostscript.com/>

This is not legal advice.
