"""
License definitions with descriptions, pros, and cons.
These are the most common open source licenses supported by GitHub.
"""

LICENSES = {
    "mit": {
        "name": "MIT License",
        "spdx_id": "MIT",
        "description": "A short and simple permissive license with conditions only requiring preservation of copyright and license notices.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice"
        ],
        "limitations": [
            "No liability",
            "No warranty"
        ],
        "pros": [
            "Very permissive - minimal restrictions",
            "Simple and easy to understand",
            "Widely recognized and accepted",
            "Compatible with most other licenses",
            "Great for maximum adoption"
        ],
        "cons": [
            "No patent protection",
            "No copyleft - derivatives can be proprietary",
            "Minimal protection for original author"
        ],
        "best_for": "Projects wanting maximum adoption with minimal restrictions"
    },
    "apache-2.0": {
        "name": "Apache License 2.0",
        "spdx_id": "Apache-2.0",
        "description": "A permissive license that also provides an express grant of patent rights from contributors to users.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Patent use",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice",
            "State changes"
        ],
        "limitations": [
            "No liability",
            "No warranty",
            "No trademark use"
        ],
        "pros": [
            "Explicit patent grant protection",
            "Clear contribution terms",
            "Protects against patent trolls",
            "Business-friendly",
            "Widely used in enterprise"
        ],
        "cons": [
            "Longer and more complex than MIT",
            "No copyleft protection",
            "Incompatible with GPLv2"
        ],
        "best_for": "Projects needing patent protection, enterprise use"
    },
    "gpl-3.0": {
        "name": "GNU General Public License v3.0",
        "spdx_id": "GPL-3.0",
        "description": "A strong copyleft license that requires derived works to be open-sourced under the same license.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Patent use",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice",
            "State changes",
            "Disclose source",
            "Same license"
        ],
        "limitations": [
            "No liability",
            "No warranty"
        ],
        "pros": [
            "Strong copyleft - keeps code open",
            "Patent protection included",
            "Prevents proprietary forks",
            "Large community support",
            "Ensures freedom for end users"
        ],
        "cons": [
            "Incompatible with proprietary software",
            "Complex license terms",
            "May limit commercial adoption",
            "Viral nature can be restrictive"
        ],
        "best_for": "Projects that must remain open source forever"
    },
    "lgpl-3.0": {
        "name": "GNU Lesser General Public License v3.0",
        "spdx_id": "LGPL-3.0",
        "description": "A weaker copyleft license that allows linking from proprietary software while keeping the library itself open.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Patent use",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice",
            "State changes",
            "Disclose source (library only)",
            "Same license (library only)"
        ],
        "limitations": [
            "No liability",
            "No warranty"
        ],
        "pros": [
            "Library can be used in proprietary software",
            "Modifications to library stay open",
            "Good balance of freedom and adoption",
            "Widely used for libraries"
        ],
        "cons": [
            "Complex linking requirements",
            "Less protection than full GPL",
            "Can be confusing to comply with"
        ],
        "best_for": "Libraries that want wide adoption but stay open"
    },
    "bsd-3-clause": {
        "name": "BSD 3-Clause License",
        "spdx_id": "BSD-3-Clause",
        "description": "A permissive license similar to MIT but with an additional clause preventing use of contributor names for endorsement.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice"
        ],
        "limitations": [
            "No liability",
            "No warranty",
            "No endorsement"
        ],
        "pros": [
            "Very permissive like MIT",
            "Protects contributor names",
            "BSD heritage - well established",
            "Compatible with GPL"
        ],
        "cons": [
            "No patent protection",
            "No copyleft",
            "Slightly more restrictive than MIT"
        ],
        "best_for": "Academic and research projects"
    },
    "bsd-2-clause": {
        "name": "BSD 2-Clause \"Simplified\" License",
        "spdx_id": "BSD-2-Clause",
        "description": "A simplified version of BSD-3-Clause without the non-endorsement clause.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice"
        ],
        "limitations": [
            "No liability",
            "No warranty"
        ],
        "pros": [
            "Simpler than BSD-3-Clause",
            "Functionally similar to MIT",
            "Minimal restrictions"
        ],
        "cons": [
            "No patent protection",
            "No copyleft",
            "Less common than MIT"
        ],
        "best_for": "Simple projects wanting BSD branding"
    },
    "mpl-2.0": {
        "name": "Mozilla Public License 2.0",
        "spdx_id": "MPL-2.0",
        "description": "A weak copyleft license that allows mixing with proprietary code, but modified files must stay open.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Patent use",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice",
            "Disclose source (modified files)"
        ],
        "limitations": [
            "No liability",
            "No warranty",
            "No trademark use"
        ],
        "pros": [
            "File-level copyleft (flexible)",
            "Can combine with proprietary code",
            "Patent protection included",
            "Compatible with GPL",
            "Good middle ground"
        ],
        "cons": [
            "More complex than MIT/Apache",
            "Less well-known",
            "File-level tracking required"
        ],
        "best_for": "Projects wanting copyleft flexibility"
    },
    "unlicense": {
        "name": "The Unlicense",
        "spdx_id": "Unlicense",
        "description": "A public domain dedication - no conditions whatsoever, maximum freedom.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Private use"
        ],
        "conditions": [],
        "limitations": [
            "No liability",
            "No warranty"
        ],
        "pros": [
            "Maximum freedom - public domain",
            "No attribution required",
            "Simplest possible terms",
            "No restrictions at all"
        ],
        "cons": [
            "No protection for author",
            "Public domain not recognized everywhere",
            "No patent protection",
            "May have legal uncertainty in some jurisdictions"
        ],
        "best_for": "Code snippets, examples, utilities"
    },
    "agpl-3.0": {
        "name": "GNU Affero General Public License v3.0",
        "spdx_id": "AGPL-3.0",
        "description": "The strongest copyleft license - requires source disclosure even for network/server use.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Patent use",
            "Private use"
        ],
        "conditions": [
            "License and copyright notice",
            "State changes",
            "Disclose source",
            "Same license",
            "Network use is distribution"
        ],
        "limitations": [
            "No liability",
            "No warranty"
        ],
        "pros": [
            "Closes the SaaS loophole",
            "Strongest open source protection",
            "Prevents proprietary cloud services",
            "Ensures all users get source"
        ],
        "cons": [
            "Very restrictive for businesses",
            "May severely limit adoption",
            "Complex compliance requirements",
            "Often avoided by enterprises"
        ],
        "best_for": "SaaS/web apps that must stay open source"
    },
    "cc0-1.0": {
        "name": "Creative Commons Zero v1.0 Universal",
        "spdx_id": "CC0-1.0",
        "description": "A public domain dedication with a fallback license for jurisdictions that don't recognize public domain.",
        "permissions": [
            "Commercial use",
            "Modification",
            "Distribution",
            "Private use"
        ],
        "conditions": [],
        "limitations": [
            "No liability",
            "No warranty",
            "No patent rights"
        ],
        "pros": [
            "True public domain dedication",
            "Legally robust fallback",
            "No attribution needed",
            "Works internationally"
        ],
        "cons": [
            "No protection for author",
            "No patent grant",
            "Originally for creative works"
        ],
        "best_for": "Data, documentation, simple utilities"
    }
}

# Order for display (most common first)
LICENSE_ORDER = [
    "mit",
    "apache-2.0",
    "gpl-3.0",
    "bsd-3-clause",
    "lgpl-3.0",
    "mpl-2.0",
    "agpl-3.0",
    "bsd-2-clause",
    "unlicense",
    "cc0-1.0"
]


def get_license_list():
    """Get ordered list of licenses for display"""
    return [(key, LICENSES[key]) for key in LICENSE_ORDER]


def get_license_by_id(license_id: str):
    """Get license info by SPDX ID or key"""
    # Try direct key lookup
    if license_id.lower() in LICENSES:
        return LICENSES[license_id.lower()]
    
    # Try SPDX ID lookup
    for key, license_info in LICENSES.items():
        if license_info["spdx_id"].lower() == license_id.lower():
            return license_info
    
    return None
