"""
Collected rules from RFC 9309
https://datatracker.ietf.org/doc/rfc9309
"""

from abnf.parser import Rule as _Rule
from . import rfc3986
from .misc import load_grammar_rulelist


@load_grammar_rulelist(
    [
        ("URI-reference", rfc3986.Rule("URI-reference")),
        ("uri", rfc3986.Rule("uri")),
    ]
)
class Rule(_Rule):
    """Rules from RFC 9309"""

    grammar = r"""
robotstxt = *(group / emptyline)
group = startgroupline                ; We start with a user-agent
                                      ; line
       *(startgroupline / emptyline)  ; ... and possibly more
                                      ; user-agent lines
       *(rule / emptyline)            ; followed by rules relevant
                                      ; for the preceding
                                      ; user-agent lines

startgroupline = *WS "user-agent" *WS ":" *WS product-token EOL

rule = *WS ("allow" / "disallow") *WS ":"
      *WS (path-pattern / empty-pattern) EOL

sitemap = *WS "sitemap" *WS ":" *WS uri EOL

; parser implementors: define additional lines you need (for
; example, Sitemaps).

product-token = identifier / "*"
path-pattern = "/" *UTF8-char-noctl ; valid URI path pattern
empty-pattern = *WS

identifier = 1*(%x2D / %x41-5A / %x5F / %x61-7A)
comment = "#" *(UTF8-char-noctl / WS / "#")
emptyline = EOL
EOL = *WS [comment] NL ; end-of-line may have
                       ; optional trailing comment
NL = %x0D / %x0A / %x0D.0A
WS = %x20 / %x09
uri = <uri, see [RFC3986], Section 3>

; UTF8 derived from RFC 3629, but excluding control characters

UTF8-char-noctl = UTF8-1-noctl / UTF8-2 / UTF8-3 / UTF8-4
UTF8-1-noctl = %x21 / %x22 / %x24-7F ; excluding control, space, "#"
UTF8-2 = %xC2-DF UTF8-tail
UTF8-3 = %xE0 %xA0-BF UTF8-tail / %xE1-EC 2UTF8-tail /
         %xED %x80-9F UTF8-tail / %xEE-EF 2UTF8-tail
UTF8-4 = %xF0 %x90-BF 2UTF8-tail / %xF1-F3 3UTF8-tail /
         %xF4 %x80-8F 2UTF8-tail

UTF8-tail = %x80-BF


    """