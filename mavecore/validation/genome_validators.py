"""
Validator functions for the fields of the following classes:
    WildTypeSequence
    ReferenceGenome
    TargetGene
    ReferenceMap
    GenomicInterval

Most validation should validate one specific field, unless fields need
to be validated against each other.
"""
import re
from fqfa.validator.validator import dna_bases_validator, amino_acids_validator
from mavecore.validation.exceptions import ValidationError

from mavecore.validation import constants


def is_null(value):
    """
    This function checks if the value exists or is null.

    Parameters
    __________
    value :
        The value to be checked.

    Returns
    _______

    """
    value = str(value).strip().lower()
    return constants.null_values_re.fullmatch(value) or not value


# min_start_validator = MinValueValidator(
#    1, message=_("Start coordinate must be a positive integer.")
# )
# min_end_validator = MinValueValidator(
#    1, message=_("End coordinate must be a positive integer.")
# )


class WildTypeSequence:
    """
    Basic model specifying a wild-type sequence.

    Parameters
    ----------
    sequence : `models.CharField`
        The wild type DNA sequence that is related to the `target`. Will
        be converted to upper-case upon instantiation.

    sequence_type : `models.CharField`
        Protein sequence (amino acids) or DNA (nucleotides)
    """

    class SequenceType:
        """

        """
        DNA = "dna"
        PROTEIN = "protein"
        INFER = "infer"

        @classmethod
        def detect_sequence_type(cls, sequence):
            """

            Parameters
            __________
            sequence :

            Returns
            _______

            Raises
            ______
            ValueError
                If sequence parameter is not protein or DNA
            """
            if sequence_is_dna(sequence):
                return cls.DNA
            elif sequence_is_protein(sequence):
                return cls.PROTEIN
            else:
                raise ValueError(
                    f"Unknown sequence '{sequence}'. It is not protein or DNA."
                )

        @classmethod
        def is_protein(cls, value):
            """

            Parameters
            __________
            value :

            Returns
            _______

            """
            return value == cls.PROTEIN

        @classmethod
        def is_dna(cls, value):
            """

            Parameters
            __________
            value :

            Returns
            _______

            """
            return value == cls.DNA

        @classmethod
        def choices(cls):
            """

            Returns
            _______
            """
            return [(cls.INFER, "Infer"), (cls.DNA, "DNA"), (cls.PROTEIN, "Protein")]

    class Meta:
        """

        """
        verbose_name = "Reference sequence"
        verbose_name_plural = "Reference sequences"

    def __str__(self):
        """

        Returns
        _______

        """
        return self.get_sequence()

    # sequence = models.TextField(
    #    default=None,
    #    blank=False,
    #    null=False,
    #    verbose_name="Reference sequence",
    #    validation=[validate_wildtype_sequence],
    # )
    # sequence_type = models.CharField(
    #    blank=True,
    #    null=False,
    #    default=SequenceType.INFER,
    #    verbose_name="Reference sequence type",
    #    max_length=32,
    #    choices=SequenceType.choices(),
    # )

    @property
    def is_dna(self):
        """

        Returns
        _______

        """
        return self.__class__.SequenceType.is_dna(self.sequence_type)

    @property
    def is_protein(self):
        """

        Returns
        _______

        """
        return self.__class__.SequenceType.is_protein(self.sequence_type)

    def save(self, *args, **kwargs):
        """

        Parameters
        __________
        args :
        kwargs :

        Returns
        _______

        """
        if self.sequence is not None:
            self.sequence = self.sequence.upper()
            self.sequence_type = (
                (self.__class__.SequenceType.detect_sequence_type(self.sequence))
                if self.__class__.SequenceType.INFER
                else self.sequence_type
            )

        return super().save(*args, **kwargs)

    def get_sequence(self):
        """

        Returns
        _______

        """
        return self.sequence.upper()

    def is_attached(self):
        """

        Returns
        _______

        """
        return getattr(self, "target", None) is not None


# GenomicInterval
# ------------------------------------------------------------------------- #
def validate_interval_start_lteq_end(start, end):
    """

    Parameters
    __________
    start :
    end :

    Returns
    _______

    Raises
    ______
    ValidationError
        If an interval's starting coordinate is greater than the ending coordinate.
    """
    # Intervals may be underspecified, but will be ignored so skip validation.
    if start is None or end is None:
        return
    if start > end:
        raise ValidationError(
            (
                "An interval's starting coordinate cannot be greater than the "
                "ending coordinate."
            )
        )


def validate_strand(value):
    """

    Parameters
    __________
    value :

    Raises
    ______
    ValidationError
        If GenomicInterval strand is not positive or negative.
    """
    if value not in ("+", "-"):
        raise ValidationError("GenomicInterval strand must be either '+' or '-'")


def validate_chromosome(value):
    """

    :param value:
    :return:
    """
    # Intervals may be underspecified, but will be ignored so skip validation.
    if value is None:
        return
    if is_null(value):
        raise ValidationError("Chromosome identifier must not be null.")


def validate_unique_intervals(intervals):
    """

    :param intervals:
    :return:
    """
    for interval1 in intervals:
        for interval2 in intervals:
            if (
                (interval1.pk is not None)
                and (interval2.pk is not None)
                and (interval1.pk == interval2.pk)
            ):
                continue
            elif interval1 is interval2:
                continue
            elif interval1.equals(interval2):
                raise ValidationError("You can not specify the same interval twice.")


# WildTypeSequence
# ------------------------------------------------------------------------- #
def validate_wildtype_sequence(seq, as_type="any"):
    """

    :param seq:
    :param as_type:
    :return:
    """
    # from .models import WildTypeSequence

    # Explicitly check for these cases as they are also valid AA sequences.
    if is_null(seq):
        raise ValidationError(
            "'%(seq)s' is not a valid wild type sequence."  # , params={"seq": seq}
        )

    seq = seq.upper()
    is_dna = dna_bases_validator(seq) is not None
    is_aa = amino_acids_validator(seq) is not None

    if as_type == WildTypeSequence.SequenceType.DNA and not is_dna:
        raise ValidationError(
            "'%(seq)s' is not a valid DNA reference sequence."  # ,
            # params={"seq": seq},
        )
    elif as_type == WildTypeSequence.SequenceType.PROTEIN and not is_aa:
        raise ValidationError(
            "'%(seq)s' is not a valid protein reference sequence."  # ,
            # params={"seq": seq},
        )
    elif (as_type == "any" or WildTypeSequence.SequenceType.INFER) and not (
        is_dna or is_aa
    ):
        raise ValidationError(
            "'%(seq)s' is not a valid DNA or protein reference sequence."  # ,
            # params={"seq": seq},
        )


def sequence_is_dna(seq):
    """

    :param seq:
    :return:
    """
    # Explicitly check for these cases as they are also valid AA sequences.
    if is_null(seq):
        return False
    seq = seq.upper()
    return dna_bases_validator(seq) is not None


def sequence_is_protein(seq):
    """

    :param seq:
    :return:
    """
    # Explicitly check for these cases as they are also valid AA sequences.
    if is_null(seq):
        return False
    seq = seq.upper()
    if dna_bases_validator(seq) is not None:
        return False  # Very likely a DNA sequence if only ATG
    return amino_acids_validator(seq) is not None


# ReferenceGenome
# ------------------------------------------------------------------------- #
def validate_organism_name(value):
    """

    :param value:
    :return:
    """
    if is_null(value):
        raise ValidationError("Species name must not be null.")


def validate_reference_genome_has_one_external_identifier(referencegenome):
    """

    :param referencegenome:
    :return:
    """
    if not referencegenome.genome_id:
        raise ValidationError(
            "Only one external identifier can be specified for a reference" "genome."
        )


def validate_genome_short_name(value):
    """

    :param value:
    :return:
    """
    if is_null(value):
        raise ValidationError("Genome short name must not be null.")


# ReferenceMap
# ------------------------------------------------------------------------- #
def validate_map_has_unique_reference_genome(annotations):
    """

    :param annotations:
    :return:
    """
    genomes = set([str(a.get_reference_genome_name()).lower() for a in annotations])
    if len(genomes) < len(annotations):
        raise ValidationError(
            "Each reference map must specify a different reference genome."
        )


def validate_map_has_at_least_one_interval(reference_map):
    """

    :param reference_map:
    :return:
    """
    if not reference_map.get_intervals().count():
        raise ValidationError(
            "You must specify at least one interval for each reference map."
        )


def validate_at_least_one_map(reference_maps):
    """

    :param reference_maps:
    :return:
    """
    if not len(reference_maps):
        raise ValidationError(
            "A target must have at least one reference map specified."
        )


def validate_one_primary_map(reference_maps):
    """
    This function validates the existence of one primary reference map and raises an error
    if it does not exist.

    Parameters
    __________
    reference_maps :

    Raises
    ______
    ValidationError
        If target has less than or more than one primary reference map.
    """
    primary_count = sum(a.is_primary_reference_map() for a in reference_maps)
    if primary_count > 1 or primary_count < 1:
        raise ValidationError("A target must have one primary reference map.")


# TargetGene
# ------------------------------------------------------------------------- #
def validate_gene_name(value):
    """
    This function checks to see if a gene name is null and raises and error if it is.

    Parameters
    __________
    value :
        The gene name.

    Raises
    ______
    ValidationError
        If gene name (value parameter) is null.
    """
    if is_null(value):
        raise ValidationError("Gene name must not be null.")
