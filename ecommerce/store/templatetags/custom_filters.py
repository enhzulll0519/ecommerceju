from django import template

register = template.Library()

@register.filter
def stars(rating):
    """ Returns stars based on the rating value. """
    try:
        # Rating нь integer утга болгох
        rating = int(rating)
    except (ValueError, TypeError):
        rating = 0  # Хэрэв буруу утга ирвэл 0 гэж үзнэ

    filled_stars = "★" * rating  # Дүүрсэн од
    empty_stars = "☆" * (5 - rating)  # Хоосон од
    return filled_stars + empty_stars
