from mavecore.validation.constants.general import null_values_re
from random import choice

from mavehgvs.variant import Variant
from mavecore.validation.variant import validate_hgvs_string
from mavecore.validation.constants.conversion import codon_dict_DNA


def is_null(value):
    """
    Returns True if a stripped/lowercase value in in `nan_col_values`.

    Parameters
    __________
    value : str
        The value to be checked as null or not.

    Returns
    _______
    bool
        True value is NoneType or if value matches the stated regex patterns in constants.null_values_re.
    """
    value = str(value).strip().lower()
    return null_values_re.fullmatch(value) or not value


def generate_hgvs(prefix: str = "c") -> str:
    """
    Generates a random hgvs string from a small sample.
    """
    if prefix == "p":
        # Subset of 3-letter codes, chosen at random.
        amino_acids = [
            "Ala",
            "Leu",
            "Gly",
            "Val",
            "Tyr",
            "Met",
            "Cys",
            "His",
            "Glu",
            "Phe",
        ]
        ref = choice(amino_acids)
        alt = choice(amino_acids)
        return f"{prefix}.{ref}{choice(range(1, 100))}{alt}"
    else:
        alt = choice("ATCG")
        ref = choice("ATCG")
        return f"{prefix}.{choice(range(1, 100))}{ref}>{alt}"


def construct_hgvs_pro(wt, mutant, position: int):
    #if pd.isna(position): return None
    if wt == mutant:
        hgvs = "p." + wt + str(position) + "="
    else:
        hgvs = "p." + wt + str(position) + mutant
    # validate variant
    validate_hgvs_string(hgvs)
    return hgvs #, hgvs_validate


def get_codon_data_from_nt_variants(hgvs_nt, target_seq):
    """
    This method takes in a target sequence and converts coding variants into codon changes.
    These changes are stored in three additional MaveDf columns: target_codon, codon_number, and variant_codon.
    This method also updates the hgvs from legacy to mave hgvs, if it is not already done.

    Parameters
    __________
    target_seq : string
        target sequence

    Raises
    ______
    TypeError
        if target_seq is not string
    ValueError
        if target_seq is not made solely of characters ACTG
    """
    # check for TypeError
    # if target_seq is not string
    if not isinstance(target_seq, str):
        raise TypeError("target_seq must be string")

    # check for ValueError
    # if target_seq is not made solely of characters ACTG
    check_chars = [letter in "ACTG" for letter in target_seq]
    if False in check_chars:
        raise ValueError("target_seq is invalid")

    # identify variant_position and get codon_number associated with it

    if is_wild_type(hgvs_nt):  # variant_codon is wild-type
        codon_number = None
        target_codon = None
    else:  # any other variant change
        # instantiate Variant object
        variant = Variant(hgvs_nt)
        # get variant position and convert to int
        if type(variant.positions) == list:  # multiple positions values exist
            variant_position = int(str(variant.positions[0]))
        elif type(variant.positions) == tuple:
            variant_position = int(str(variant.positions[0]))
        else:  # only one value for positions
            variant_position = int(str(variant.positions))
        # now that we have the variant_position, get codon_number
        codon_number = round((variant_position / 3) + 0.5)
        # use codon_number to get target_codon from target_seq
        target_codon = target_seq[(codon_number - 1) * 3 : codon_number * 3]

    # determine sequence of variant_codon

    if is_wild_type(hgvs_nt):  # variant_codon is wild-type
        variant_codon = target_codon
        sub_one = None  # no nucleotide substitutions
    elif is_deletion(hgvs_nt):  # target_codon was deleted
        variant_codon = None
        sub_one = None  # no nucleotide substitutions
    elif is_substitution_one_base(
        hgvs_nt
    ):  # variant_codon has one nucleotide substitution
        # instantiate Variant object
        variant = Variant(hgvs_nt)
        # get index of nucleotide substitution
        sub_one = int(str(variant.positions)) % 3 - 1
        # get nucleotide of substitution
        sub_one_nuc = variant.sequence[1]
        # set other possible indices for codon substitution to None
        sub_two = None
        sub_three = None
    elif is_substitution_two_bases_nonadjacent(
        hgvs_nt
    ):  # variant has two nucleotide substitutions, non-adjacent
        # instantiate Variant object
        variant = Variant(hgvs_nt)
        # get indices of nucleotide substitutions
        sub_one = int(str(variant.positions[0])) % 3 - 1
        sub_two = int(str(variant.positions[1])) % 3 - 1
        # get nucleotides of substitutions
        sub_one_nuc = variant.sequence[0][1]
        sub_two_nuc = variant.sequence[1][1]
        # set other possible indices for codon substitution to None
        sub_three = None
    else:  # variant_codon has two or three adjacent nucleotide substitutions
        # instantiate Variant object
        variant = Variant(hgvs_nt)
        variant_codon = variant.sequence
        # get index of first codon substitution
        sub_one = int(str(variant.positions[0])) % 3 - 1
        # get string of substituted nucleotides
        sub_nucs = variant.sequence
        if (
            len(sub_nucs) == 2
        ):  # variant codon has two adjacent nucleotide substitutions
            # assign additional nucleotide substitution indices
            sub_two = sub_one + 1
            # get nucleotides of substitutions
            sub_one_nuc = sub_nucs[0]
            sub_two_nuc = sub_nucs[1]
            # set other possible indices for codon substitution to None
            sub_three = None
        else:  # variant has three adjacent nucleotide substitutions
            # assign additional nucleotide substitution indices
            sub_two = sub_one + 1
            sub_three = sub_two + 1
            # get nucleotides of substitutions
            sub_one_nuc = sub_nucs[0]
            sub_two_nuc = sub_nucs[1]
            sub_three_nuc = sub_nucs[2]

    # using data generated above (substituted nucleotides and indices in codon), construct variant_codon

    # only assign variant_codon if nucleotide substitution occurred
    if sub_one is not None:
        # declare and initialize variant_codon
        variant_codon = ""
        # set first nucleotide of variant_codon
        if sub_one == 0:
            variant_codon = variant_codon + sub_one_nuc
        else:
            variant_codon = variant_codon + target_codon[0]
        # set second nucleotide of variant_codon
        if sub_one == 1:
            variant_codon = variant_codon + sub_one_nuc
        elif sub_two == 1:
            variant_codon = variant_codon + sub_two_nuc
        else:
            variant_codon = variant_codon + target_codon[1]
        # set third nucleotide of variant_codon
        if sub_one == -1 or sub_one == 2:
            variant_codon = variant_codon + sub_one_nuc
        elif sub_two == -1 or sub_two == 2:
            variant_codon = variant_codon + sub_two_nuc
        elif sub_three == -1 or sub_three == 2:
            variant_codon = variant_codon + sub_three_nuc
        else:
            variant_codon = variant_codon + target_codon[2]

    # add values for target_codon, codon_number, and variant_codon to this row
    return target_codon, codon_number, variant_codon


def is_wild_type(hgvs):
    """
    This function takes an hgvs formatted string and returns True if the hgvs string indicates
    there was no change from the target sequence.

    Parameters
    ----------
    hgvs : string
        hgvs formatted string

    Returns
    -------
    wt : bool
        True if hgvs string indicates wild type
    """
    wt = False
    if hgvs.startswith("_wt"):
        wt = True
    return wt


def is_deletion(hgvs):
    """
    This function takes an hgvs formatted string and returns True if the hgvs string indicates
    there was a deletion.

    Parameters
    ----------
    hgvs : string
        hgvs formatted string

    Returns
    -------
    deletion : bool
        True if hgvs string is indicates a deletion
    """
    deletion = False
    if hgvs.endswith("del"):
        deletion = True
    return deletion


def is_substitution_one_base(hgvs):
    """
    This function takes an hgvs formatted string and returns True if the hgvs string indicates
    there was a substitution at one base of the codon.

    Parameters
    ----------
    hgvs : string
        hgvs formatted string

    Returns
    -------
    sub_one : bool
        True if hgvs string is indicates a substitution at one base of codon
    """
    sub_one = False
    if hgvs[-2] == ">":
        sub_one = True
    return sub_one


def is_substitution_two_bases_nonadjacent(hgvs):
    """
    This function takes an hgvs formatted string and returns True if the hgvs string indicates
    there were substitutions (non-adjacent) in the codon.

    Parameters
    ----------
    hgvs : string
        hgvs formatted string

    Returns
    -------
    sub_two : bool
        True if hgvs string is indicates a substitution at one base of codon
    """
    sub_two = False
    if hgvs[-1] == "]":
        sub_two = True
    return sub_two
