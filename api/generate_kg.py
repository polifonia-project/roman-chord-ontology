"""

"""
from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import FOAF, RDF, RDFS, OWL


def generate_kg(decomposed_roman: dict):
    """

    :return:
    """
    ROMAN = Namespace('http://w3id.org/polifonia/ontology/roman-chord/')
    CHORD = Namespace('http://purl.org/ontology/chord/')
    g = Graph()
    g.bind('roman', ROMAN)
    g.bind('chord', CHORD)

    roman_chord = URIRef(f'http://w3id.org/polifonia/ontology/roman-chord/{decomposed_roman["chord"]}')
    quality = URIRef(f'http://w3id.org/polifonia/resource/jams/{decomposed_roman["quality"]}')
    inversion = Literal(decomposed_roman['inversion'])
    basic_function = URIRef(f'http://w3id.org/polifonia/resource/jams/{decomposed_roman["plain_roman"]}')
    basic_function_name = Literal(decomposed_roman["plain_roman"])
    root_note = URIRef(f'http://purl.org/ontology/chord/{decomposed_roman["root"]}')
    bass = BNode()
    bass_alteration, bass_degree = decomposed_roman["bass"]
    bass_interval = URIRef(f'http://w3id.org/polifonia/resource/jams/{"".join([x for x in decomposed_roman["bass"]])}')
    bass_degree = Literal(bass_degree)

    # roman chord
    g.add((roman_chord, RDF.type, ROMAN.Chord))
    g.add((roman_chord, ROMAN.hasQuality, quality))
    g.add((roman_chord, ROMAN.inversionType, inversion))
    g.add((roman_chord, ROMAN.hasBasicFunction, basic_function))
    g.add((roman_chord, ROMAN.hasRoot, root_note))
    g.add((roman_chord, ROMAN.hasBass, bass_interval))
    # basic function
    g.add((basic_function, RDFS.label, basic_function_name))
    # bass interval
    g.add((bass_interval, RDF.type, ROMAN.Interval))
    g.add((bass_interval, ROMAN.hasDegree, bass_degree))
    if bass_alteration != '':
        bass_alteration = Literal(bass_alteration)
        g.add((bass_interval, ROMAN.hasModifier, bass_alteration))
    # intervals
    for interval in decomposed_roman['degrees']:
        interval_uri = URIRef(f'http://w3id.org/polifonia/resource/jams/{"".join([x for x in interval])}')
        interval_alteration, interval_degree = interval
        g.add((roman_chord, ROMAN.containsInterval, interval_uri))
        g.add((interval_uri, ROMAN.hasDegree, Literal(interval_degree)))
        if interval_alteration != '':
            g.add((interval_uri, ROMAN.hasModifier, Literal(interval_alteration)))
    # missing intervals
    for missing_interval in decomposed_roman['missing']:
        missing_interval_uri = URIRef(f'http://w3id.org/polifonia/resource/jams/{"".join([x for x in missing_interval])}')
        missing_interval_alteration, missing_interval_degree = missing_interval
        g.add((roman_chord, ROMAN.containsInterval, Literal(missing_interval_uri)))
        g.add((missing_interval_uri, ROMAN.hasDegree, Literal(missing_interval_degree)))
        if missing_interval_alteration != '':
            g.add((missing_interval_uri, ROMAN.hasModifier, Literal(missing_interval_alteration)))

    return g.serialize()


if __name__ == '__main__':
    # test the script
    dummy_chord = {'chord': 'VII64[no3]', 'quality': 'other', 'inversion': 2, 'plain_roman': 'VII', 'root': 'B#', 'bass': ('##', '4'), 'degrees': [('##', '4'), ('#', '7')], 'missing': [('', '3')]}
    test_kg = generate_kg(dummy_chord)
    print(test_kg)
