"""

"""
from pydantic import BaseModel, ValidationError
from rdflib import Graph, URIRef, Literal, BNode, Namespace, exceptions
from rdflib.namespace import RDF, RDFS, OWL


class DecomposedChordModel(BaseModel):
    roman_chord: dict


def generate_kg(decomposed_roman: dict):
    """

    :return:
    """

    decomposed_roman = DecomposedChordModel(roman_chord=decomposed_roman)
    decomposed_roman = decomposed_roman.roman_chord

    try:
        ROMAN = Namespace('http://w3id.org/polifonia/ontology/roman-chord/')
        CHORD = Namespace('http://purl.org/ontology/chord/')
        g = Graph()
        g.bind('roman', ROMAN)
        g.bind('chord', CHORD)

        roman_chord = URIRef(f'http://w3id.org/polifonia/resource/roman-chord/{decomposed_roman["chord"]}')
        quality = URIRef(f'http://w3id.org/polifonia/resource/roman-chord/{decomposed_roman["quality"]}')
        inversion = Literal(decomposed_roman['inversion'])
        basic_function_name = Literal(decomposed_roman["plain_roman"])
        root_note = URIRef(
            f'http://purl.org/ontology/chord/{"".join([x if x is not None else "" for x in decomposed_roman["root"]])}')
        bass_alteration, bass_degree = decomposed_roman["bass"]
        bass_degree = Literal(bass_degree)

        # roman chord
        g.add((roman_chord, RDF.type, ROMAN.Chord))
        g.add((roman_chord, ROMAN.hasQuality, quality))
        g.add((roman_chord, ROMAN.inversionType, inversion))
        g.add((roman_chord, ROMAN.hasRoot, root_note))
        # basic function
        basic_node = BNode()
        g.add((roman_chord, ROMAN.hasBasicFunction, basic_node))
        g.add((basic_node, RDFS.label, basic_function_name))
        g.add((basic_node, RDF.type, ROMAN.BasicFunction))
        # bass interval
        bass = BNode()
        g.add((roman_chord, ROMAN.hasBass, bass))
        g.add((bass, RDF.type, ROMAN.Interval))
        g.add((bass, CHORD.degree, bass_degree))
        g.add((bass, OWL.sameAs,
               URIRef(
                   f'http://purl.org/ontology/scale_interval/{"".join([x if x is not None else "" for x in bass])}')))
        if bass_alteration is not None:
            bass_alteration = Literal(bass_alteration)
            g.add((bass, CHORD.modifier, bass_alteration))
        # intervals
        for interval in decomposed_roman['degrees']:
            interval_node = BNode()
            interval_alteration, interval_degree = interval
            g.add((roman_chord, ROMAN.containsInterval, interval_node))
            g.add((interval_node, RDF.type, ROMAN.Interval))
            g.add((interval_node, OWL.sameAs, URIRef(
                f'http://purl.org/ontology/scale_interval/{"".join([x if x is not None else "" for x in interval])}')))
            g.add((interval_node, CHORD.degree, Literal(int(interval_degree))))
            if interval_alteration is not None:
                g.add((interval_node, CHORD.modifier, Literal(interval_alteration)))
        # missing intervals
        for missing_interval in decomposed_roman['missing']:
            missing_node = BNode()
            missing_interval_alteration, missing_interval_degree = missing_interval
            g.add((roman_chord, ROMAN.missingInterval, missing_node))
            g.add((missing_node, RDF.type, ROMAN.Interval))
            g.add((missing_node, OWL.sameAs, URIRef(
                f'http://purl.org/ontology/scale_interval/{"".join([x if x is not None else "" for x in missing_interval])}')))
            g.add((missing_node, CHORD.degree, Literal(int(missing_interval_degree))))
            if missing_interval_alteration is not None:
                g.add((missing_node, CHORD.modifier, Literal(missing_interval_alteration)))
    except (TypeError, exceptions.TypeCheckError, exceptions.ParserError, exceptions.UniquenessError) as e:
        raise ValueError(f'The input dictionary cannot be converted into RDF. Error: {e}')

    return g.serialize()


if __name__ == '__main__':
    # test the script
    dummy_chord = {'chord': 'VII64[no3]', 'quality': 'other', 'inversion': 2, 'plain_roman': 'VII',
                   'root': ('sharp', 'B'), 'bass': ('doublesharp', '4'),
                   'degrees': [('doublesharp', '4'), ('sharp', '7')], 'missing': [(None, '3')]}
    test_kg = generate_kg(dummy_chord)
    print(test_kg)
