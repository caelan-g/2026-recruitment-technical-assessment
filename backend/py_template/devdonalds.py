from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = []

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	final = ""
	prev = ""
	space_characters = ["_", "-", " "]
	recipeName = recipeName.strip()
	for i in range(0, len(recipeName)):
		if recipeName[i] in space_characters and prev not in space_characters:
			final += " "
		elif recipeName[i].isalpha():
			if prev in space_characters or i == 0:
				final += (recipeName[i].upper())
			else:
				final += (recipeName[i].lower())
		prev = recipeName[i]
	if len(final) > 0:
		return final
	else:
		return None


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
    data = request.get_json()
    if not data or "type" not in data:
        return jsonify({"error": "Missing type field"}), 400

    if data["type"] == "recipe":
        items = [RequiredItem(**item) for item in data.get("requiredItems", [])]
        entry = Recipe(name=data["name"], required_items=items)
        unique_names = set()
        
        for item in entry.required_items:
            name_lower = item.name.lower()
            
            if name_lower in unique_names:
                return jsonify({"error": "Required items must have unique names"}), 400
            unique_names.add(name_lower)

    elif data["type"] == "ingredient":
        entry = Ingredient(name=data["name"], cook_time=data["cookTime"])
        print(entry)
        if entry.cook_time < 0:
            return jsonify({"error": "Invalid cook time"}), 400

    else:
        return jsonify({"error": "Invalid entry type"}), 400

    if any(existing.name == entry.name for existing in cookbook):
        return jsonify({"error": "Entry name already exists"}), 400

    cookbook.append(entry)
    return jsonify({}), 200

# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	return 'not implemented', 500


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
