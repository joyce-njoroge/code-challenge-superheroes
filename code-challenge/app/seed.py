from random import choice, randint
from models import db, Hero, Power, HeroPower
from app import app

print("Seeding powers...")
powers_data = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
]

with app.app_context():
    with db.session.begin():
        for power_data in powers_data:
            power = Power(**power_data)
            db.session.add(power)

print("Seeding heroes...")
heroes_data = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"}
]

with app.app_context():
    with db.session.begin():
        for hero_data in heroes_data:
            hero = Hero(name=hero_data["name"], super_name=hero_data["super_name"])
            db.session.add(hero)

print("Adding powers to heroes...")

strengths = ["Strong", "Weak", "Average"]

with app.app_context():
    with db.session.begin():
        heroes = Hero.query.all()
        powers = Power.query.all()

        for hero in heroes:
            for _ in range(randint(1, 3)):
                power = choice(powers)
                hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths))
                db.session.add(hero_power)

print("Done seeding!")
