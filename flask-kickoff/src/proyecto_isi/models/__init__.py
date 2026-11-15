#Archivo que solo llevar una referencia a todas las tablas, para indicarle a lemic lo que debe de hacer
from proyecto_isi.models.Question import Question

#Indicamos la existencia de la tabla Question
__all__ = ["Question"]
