"""
Predefined topic lists for supported exams.
Each topic includes name, difficulty, exam weight, and description.
"""

from app.schemas.exam_config import ExamType


EXAM_TOPICS = {
    # =========================================================================
    # JEE MAIN — Physics, Chemistry, Mathematics (~15 topics)
    # =========================================================================
    ExamType.JEE_MAIN: [
        # Physics
        {
            "name": "Mechanics",
            "difficulty_level": 3,
            "exam_weight": 8.0,
            "description": "Newton's laws, work-energy theorem, rotational motion, gravitation, and fluid mechanics.",
        },
        {
            "name": "Electrodynamics",
            "difficulty_level": 4,
            "exam_weight": 8.0,
            "description": "Electrostatics, current electricity, magnetic effects, electromagnetic induction, and AC circuits.",
        },
        {
            "name": "Optics",
            "difficulty_level": 3,
            "exam_weight": 5.0,
            "description": "Ray optics, wave optics, interference, diffraction, and polarization.",
        },
        {
            "name": "Modern Physics",
            "difficulty_level": 4,
            "exam_weight": 5.0,
            "description": "Photoelectric effect, Bohr model, nuclear physics, radioactivity, and semiconductors.",
        },
        {
            "name": "Thermodynamics & Kinetic Theory",
            "difficulty_level": 3,
            "exam_weight": 5.0,
            "description": "Laws of thermodynamics, heat transfer, kinetic theory of gases, and calorimetry.",
        },
        {
            "name": "Waves & Oscillations",
            "difficulty_level": 3,
            "exam_weight": 3.0,
            "description": "Simple harmonic motion, wave motion, sound waves, standing waves, and Doppler effect.",
        },
        # Chemistry — Physical
        {
            "name": "Physical Chemistry",
            "difficulty_level": 3,
            "exam_weight": 12.0,
            "description": "Atomic structure, chemical bonding, thermodynamics, equilibrium, kinetics, and electrochemistry.",
        },
        # Chemistry — Organic
        {
            "name": "Organic Chemistry",
            "difficulty_level": 4,
            "exam_weight": 12.0,
            "description": "Hydrocarbons, functional groups, reaction mechanisms (SN1/SN2/E1/E2), polymers, and biomolecules.",
        },
        # Chemistry — Inorganic
        {
            "name": "Inorganic Chemistry",
            "difficulty_level": 3,
            "exam_weight": 10.0,
            "description": "Periodic table trends, coordination compounds, metallurgy, p-block and d-block elements.",
        },
        # Mathematics
        {
            "name": "Algebra",
            "difficulty_level": 3,
            "exam_weight": 8.0,
            "description": "Quadratics, sequences & series, complex numbers, matrices & determinants, permutations & combinations.",
        },
        {
            "name": "Calculus",
            "difficulty_level": 4,
            "exam_weight": 10.0,
            "description": "Limits, continuity, differentiation, integration, differential equations, and area under curves.",
        },
        {
            "name": "Coordinate Geometry",
            "difficulty_level": 3,
            "exam_weight": 6.0,
            "description": "Straight lines, circles, parabola, ellipse, and hyperbola.",
        },
        {
            "name": "Trigonometry",
            "difficulty_level": 3,
            "exam_weight": 4.0,
            "description": "Trigonometric functions, identities, equations, inverse trig functions, and properties of triangles.",
        },
        {
            "name": "Vectors & 3D Geometry",
            "difficulty_level": 3,
            "exam_weight": 4.0,
            "description": "Vector algebra, scalar and vector products, 3D coordinate geometry, lines and planes in space.",
        },
    ],

    # =========================================================================
    # JEE ADVANCED — Physics, Chemistry, Mathematics (~15 topics)
    # More advanced, conceptual depth
    # =========================================================================
    ExamType.JEE_ADVANCED: [
        # Physics
        {
            "name": "Classical Mechanics",
            "difficulty_level": 5,
            "exam_weight": 10.0,
            "description": "Advanced Newton's laws, constraints, pseudo forces, rigid body dynamics, and orbital mechanics.",
        },
        {
            "name": "Electricity & Magnetism",
            "difficulty_level": 5,
            "exam_weight": 10.0,
            "description": "Gauss's law, capacitors, RC/LR/LCR circuits, magnetic fields, Faraday's law, and Maxwell's equations.",
        },
        {
            "name": "Optics & Waves",
            "difficulty_level": 4,
            "exam_weight": 7.0,
            "description": "Advanced wave optics, interference patterns, diffraction, Doppler effect, and standing waves.",
        },
        {
            "name": "Thermodynamics & Statistical Mechanics",
            "difficulty_level": 4,
            "exam_weight": 6.0,
            "description": "Carnot cycle, entropy, heat engines, kinetic theory, and real gas behavior.",
        },
        {
            "name": "Modern Physics & Nuclear",
            "difficulty_level": 5,
            "exam_weight": 7.0,
            "description": "Quantum mechanics basics, hydrogen spectrum, X-rays, nuclear reactions, and mass-energy equivalence.",
        },
        # Chemistry
        {
            "name": "Advanced Physical Chemistry",
            "difficulty_level": 5,
            "exam_weight": 10.0,
            "description": "Chemical kinetics, ionic equilibrium, solid state, surface chemistry, and electrochemistry.",
        },
        {
            "name": "Advanced Organic Chemistry",
            "difficulty_level": 5,
            "exam_weight": 10.0,
            "description": "Named reactions, stereochemistry, aromatic chemistry, reaction mechanisms, and retrosynthesis.",
        },
        {
            "name": "Advanced Inorganic Chemistry",
            "difficulty_level": 4,
            "exam_weight": 7.0,
            "description": "Crystal field theory, organometallics, qualitative analysis, and extraction of metals.",
        },
        # Mathematics
        {
            "name": "Advanced Algebra",
            "difficulty_level": 5,
            "exam_weight": 8.0,
            "description": "Functional equations, inequalities, number theory, advanced PnC, and abstract algebra basics.",
        },
        {
            "name": "Advanced Calculus",
            "difficulty_level": 5,
            "exam_weight": 10.0,
            "description": "Multivariable limits, definite integrals (properties), DEs (first & second order), and area/volume.",
        },
        {
            "name": "Advanced Coordinate Geometry",
            "difficulty_level": 4,
            "exam_weight": 5.0,
            "description": "Conics (tangent/normal/chord), locus problems, parametric forms, and transformations.",
        },
        {
            "name": "Vectors & Matrices",
            "difficulty_level": 4,
            "exam_weight": 5.0,
            "description": "Vector spaces, linear transformations, eigenvalues (basic), Cayley-Hamilton theorem.",
        },
        {
            "name": "Probability & Statistics",
            "difficulty_level": 4,
            "exam_weight": 5.0,
            "description": "Conditional probability, Bayes' theorem, distributions, expected value, and variance.",
        },
    ],

    # =========================================================================
    # NEET — Physics, Chemistry, Biology (Botany + Zoology) (~15 topics)
    # =========================================================================
    ExamType.NEET: [
        # Physics
        {
            "name": "Mechanics",
            "difficulty_level": 3,
            "exam_weight": 7.0,
            "description": "Laws of motion, work & energy, rotational motion, gravitation, and properties of matter.",
        },
        {
            "name": "Electrostatics & Current Electricity",
            "difficulty_level": 3,
            "exam_weight": 7.0,
            "description": "Coulomb's law, electric field, potential, capacitance, Ohm's law, and Kirchhoff's rules.",
        },
        {
            "name": "Optics & Modern Physics",
            "difficulty_level": 3,
            "exam_weight": 6.0,
            "description": "Reflection, refraction, lenses, wave optics, photoelectric effect, and atomic models.",
        },
        # Chemistry
        {
            "name": "Physical Chemistry",
            "difficulty_level": 3,
            "exam_weight": 8.0,
            "description": "Mole concept, states of matter, thermodynamics, equilibrium, solutions, and electrochemistry.",
        },
        {
            "name": "Organic Chemistry",
            "difficulty_level": 3,
            "exam_weight": 8.0,
            "description": "IUPAC nomenclature, isomerism, hydrocarbons, haloalkanes, alcohols, aldehydes, and amines.",
        },
        {
            "name": "Inorganic Chemistry",
            "difficulty_level": 3,
            "exam_weight": 7.0,
            "description": "Periodic classification, chemical bonding, s/p/d/f block elements, and coordination compounds.",
        },
        # Biology — Botany
        {
            "name": "Cell Biology & Biomolecules",
            "difficulty_level": 3,
            "exam_weight": 8.0,
            "description": "Cell structure, cell cycle, biomolecules (proteins, nucleic acids, lipids, carbohydrates).",
        },
        {
            "name": "Plant Physiology",
            "difficulty_level": 3,
            "exam_weight": 6.0,
            "description": "Photosynthesis, respiration, plant growth & development, transport in plants, mineral nutrition.",
        },
        {
            "name": "Genetics & Evolution",
            "difficulty_level": 4,
            "exam_weight": 10.0,
            "description": "Mendelian genetics, molecular basis of inheritance, DNA replication, gene expression, and evolution.",
        },
        {
            "name": "Plant Diversity & Morphology",
            "difficulty_level": 2,
            "exam_weight": 5.0,
            "description": "Plant kingdom classification, morphology of flowering plants, anatomy of plants.",
        },
        {
            "name": "Ecology & Environment",
            "difficulty_level": 2,
            "exam_weight": 6.0,
            "description": "Ecosystems, biodiversity, environmental issues, population ecology, and ecological succession.",
        },
        # Biology — Zoology
        {
            "name": "Human Physiology",
            "difficulty_level": 4,
            "exam_weight": 10.0,
            "description": "Digestion, breathing, circulation, excretion, locomotion, neural & hormonal coordination.",
        },
        {
            "name": "Animal Diversity",
            "difficulty_level": 2,
            "exam_weight": 4.0,
            "description": "Animal kingdom classification, structural organization in animals.",
        },
        {
            "name": "Reproduction",
            "difficulty_level": 3,
            "exam_weight": 5.0,
            "description": "Reproduction in organisms, human reproduction, reproductive health.",
        },
        {
            "name": "Biotechnology & Human Welfare",
            "difficulty_level": 3,
            "exam_weight": 3.0,
            "description": "Biotechnology principles & processes, applications, microbes in human welfare, immunity.",
        },
    ],
}
