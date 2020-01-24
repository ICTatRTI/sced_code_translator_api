import re
import copy


def is_valid_sced_request(sced_code, crosswalk):
    err = False
    msg = ""

    # Get SCED code input and check format
    if re.match("[0-9]{5}", sced_code) is None:
        err = True
        msg = "Invalid SCED code format! SCED codes must be exactly 5 numeric digits"

    # Check code actually exists in crosswalk
    elif sced_code not in crosswalk:
        err = True
        msg = "SCED code '{0}' does not exist in v7 or archived codes".format(sced_code)

    return err, msg


def get_sced_v7_equivalent_codes(sced_code, crosswalk):

    # Get v7 equivalents of input SCED code
    code_info = crosswalk[sced_code]
    v7_codes = []

    # Get v7 equivalents
    if not code_info["is_archived"]:
        v7_codes.append(code_info)
    else:
        for v7_substitute in code_info["v7_substitutes"]:
            v7_codes.append(crosswalk[v7_substitute])

    # Add information about archived versions to each v7 code
    v7_codes = copy.deepcopy(v7_codes)
    for v7_code in v7_codes:
        archived_code_info = []
        for archived_code in v7_code["archived_versions"]:
            archived_code_info.append(crosswalk[archived_code])
        v7_code["archived_versions"] = archived_code_info

    return v7_codes


response_description = {
    'description' : 'This description',
    'submitted_data' : {
        'structure' : {
            'sced_code' : '5 digit SCED code to translate to SCED v7'
        }
    },
    'info' : {
        'structure' : {
            'time_elapsed' : 'time it took to calculate prediction and build response',
            'warning': 'A warning if archived SCED code could not be crosswalked to v7'
        }
    },
    'translated_codes' : {
        'description' : 'Array of equivalent SCED v7 codes, each with structure below',
        'structure' : {
            'sced_code': 'SCED course code',
            'course_title': 'SCED course title/name',
            'course_description': 'SCED course description',
            'archive_status': 'Whether code is archived or not',
            'v7_subsitutes': 'For archived codes, list of v7 codes that are equivalent',
            'archived_versions': 'For active v7 codes, list of equivalent archived codes from previous SCED versions',
            'warnings': 'warns when archived code could not be crosswalked to a SCED v7 code'
        }
    }
}
