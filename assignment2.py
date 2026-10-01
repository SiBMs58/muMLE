###########################
###### Assignment 2 #######
#####  Siebe & Mehdi #####
###########################

# Meta-model
mm_cs = """
    Dish:Class
    Step:Class
    Action:Class
    
    # 'Dish' has an attribute 'dishname'
    Dish_dishname:AttributeLink (Dish -> String) {
        name = "dishname";
        optional = False;
    }
    
    # 'Dish' has an attribute 'difficulty' above 0
    Dish_difficulty:AttributeLink (Dish -> Integer) {
        name = "difficulty";
        optional = False;
        constraint = `get_value(get_target(this)) > 0`;
    }
    
    # 'Dish' has an non-negative attribute 'cooktime'
    Dish_cooktime:AttributeLink (Dish -> Integer) {
        name = "cooktime";
        optional = False;
        constraint = `get_value(get_target(this)) >= 0`;
    }
        
    # 'Dish' has an attribute 'serves' above 0
    Dish_serves:AttributeLink (Dish -> Integer) {
        name = "serves";
        optional = False;
        constraint = `get_value(get_target(this)) > 0`;
    }
        
    # 'Dish' has at least one 'step'
    Dish_step:Association (Dish -> Step) {
        target_lower_cardinality = 1;
    }
    
    
    # 'Step' has an 'number', which sart with 1 and have no gaps
    Step_number:AttributeLink (Step -> Integer) {
        name = "number";
        optional = False;
        constraint = `get_value(get_target(this)) > 0`;
    }
    
    
    # 'Action' have a flag indication if it is attended
    Action_attended:AttributeLink (Action -> Boolean) {
        name = "attended";
        optional = False;
    }
    
    # 'Actions' are either Cutting, Cooking, Mixinig, Baking,...
    Action_type:AttributeLink (Action -> String) {
        name = "type";
        optional = False;
    }
    
    
    
"""

# Instance of the meta-model
m_cs = """
    myDish:Dish {
        dishname = "Pizza";
        difficulty = 3;
        cooktime = 120;
        serves = 2;
    }

    firstStep:Step {
        number = 1;
    }
    dishFirstStep:Dish_step (myDish -> firstStep)
"""


# To parse them as models, we first create our 'state', which is a mutable graph that will contain our models and meta-models:
from state.devstate import DevState
state = DevState()

# Next, we must load the Simple Class Diagrams (SCD) meta-meta-model into our 'state'. The SCD meta-meta-model is a meta-model for our meta-model, and it is also a meta-model for itself.
from bootstrap.scd import bootstrap_scd
print("Loading meta-meta-model...")
mmm = bootstrap_scd(state)
print("OK")


# Parse our meta-model
from concrete_syntax.textual_od import parser

print()
print("Parsing meta-model...")
mm = parser.parse_od(
    state,
    m_text=mm_cs,
    mm=mmm,
)
print("OK")

# Parse our instance of the meta-model
print()
print("Parsing model...")
m = parser.parse_od(
    state,
    m_text=m_cs,
    mm=mm,
)
print("OK")


# Check that our meta-model is a valid class diagram, perform a conformance check
from framework.conformance import Conformance, render_conformance_check_result

print()
print("Is our meta-model a valid class diagram?")
conf = Conformance(state, mm, mmm)
print(render_conformance_check_result(conf.check_nominal()))

# Check that our instance of the meta-model is a valid instance of the meta-model, perform a conformance check
print()
print("Is our model a valid instance of our meta model?")
conf = Conformance(state, m, mm)
print(render_conformance_check_result(conf.check_nominal()))

# Finally, let's check that our meta-model is a valid instance of itself:
print()
print("Is our meta-model a valid instance of itself?")
conf = Conformance(state, mm, mm)
print(render_conformance_check_result(conf.check_nominal()))


# Finally, let's render everything as PlantUML:
from concrete_syntax.plantuml import renderer as plantuml
from concrete_syntax.plantuml.make_url import make_url

uml = plantuml.render_package("Meta-model", plantuml.render_class_diagram(state, mm))
uml += plantuml.render_trace_conformance(state, mm, mmm)
print()
print("PlantUML output:", make_url(uml))
