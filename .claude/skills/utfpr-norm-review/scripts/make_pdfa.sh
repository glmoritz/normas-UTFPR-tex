#!/usr/bin/env bash
# Convert a compiled thesis to PDF/A-2b and validate it. Usage: make_pdfa.sh INPUT.pdf OUTPUT.pdf
# Needs the hyperref option `pdfa` in the source, or links are dropped by the conversion.
set -euo pipefail
in=$1; out=$2
icc=${ICC_PROFILE:-$(ls /usr/share/color/icc/ghostscript/srgb.icc /opt/homebrew/share/ghostscript/*/iccprofiles/srgb.icc /usr/local/share/ghostscript/*/iccprofiles/srgb.icc 2>/dev/null | head -1 || true)}
[ -r "$icc" ] || { echo "sRGB ICC profile not found. Set ICC_PROFILE=/path/to/srgb.icc" >&2; exit 2; }
vera=${VERAPDF:-$(command -v verapdf || echo "$HOME/bin/verapdf/verapdf")}
def=$(mktemp --suffix=.ps)
cat > "$def" <<EOF
%!
[/_objdef {icc_PDFA} /type /stream /OBJ pdfmark
[{icc_PDFA} << /N 3 >> /PUT pdfmark
[{icc_PDFA} ($icc) (r) file /PUT pdfmark
[/_objdef {OutputIntent_PDFA} /type /dict /OBJ pdfmark
[{OutputIntent_PDFA} << /Type /OutputIntent /S /GTS_PDFA1 /DestOutputProfile {icc_PDFA}
  /OutputConditionIdentifier (sRGB) /OutputCondition (sRGB IEC61966-2.1) /Info (sRGB IEC61966-2.1)
  /RegistryName (http://www.color.org) >> /PUT pdfmark
[{Catalog} <</OutputIntents [ {OutputIntent_PDFA} ]>> /PUT pdfmark
EOF
gs -q -dPDFA=2 -dBATCH -dNOPAUSE -dNOSAFER --permit-file-read="$icc" -dPDFACompatibilityPolicy=1 \
   -sColorConversionStrategy=RGB -sProcessColorModel=DeviceRGB -sOutputICCProfile="$icc" \
   -dAutoFilterColorImages=false -dColorImageFilter=/FlateEncode -dDownsampleColorImages=false \
   -sDEVICE=pdfwrite -sOutputFile="$out" "$def" "$in" 2>&1 | grep -ivE 'overprint|annotation|^$' || true
rm -f "$def"
before=$(pdfinfo -url "$in" | tail -n +2 | wc -l); after=$(pdfinfo -url "$out" | tail -n +2 | wc -l)
echo "links: $after of $before kept"
[ "$after" -ge "$before" ] || echo "WARNING: links were lost, including possibly the license link. Add the pdfa option to hyperref." >&2
if [ -x "$vera" ]; then
  "$vera" --flavour 2b --format text "$out" | cut -c1-5
else
  echo "veraPDF not found, so the file was NOT validated. Install it or set VERAPDF=/path/to/verapdf." >&2
  exit 3
fi
