# proyecto_isi
## Uso de Patrones de Diseño
En este proyecto de un sistema de preguntas y respuestas, al estilo StackOverflow, en su realizacion se han utilizado patrones de diseño para mejorar estrucuralmente al sistema y son:  
*Strategy* : Patron utilizado en la seccion de los LLMs con el fin de que una entidad `AgenteAutomatico` pueda responder con cualquiera de los LLMs dentro de el sistema ya sea `Gemini`, `OpenIA` O `LocalLLM`, intercambiandolos entre si cuando se lo requiera, sin tener que crear varias entidades AgenteAutomatico cada una con un LLM en especifico.  
*Factory Method* : utilizado en la creacion de usarios mediante `RegistroUsuarios`, permite la creacion de usuarios y administradores con una unica clase, donde sus subclases, `RegistroAdministrador` y `RegistroUsuarioGeneral`, implementan la creacion de un tipo de usuario en especifico. Esto permite que el sistema sea altamente extendible sin tener que modificar todo el codigo existente.  
## Nota
1. El modelo de dominio de el sistema fue realizado en **Astah UML**, es por ello que el archivo `preguntas_respuestas_proyecto.asta`, debe de ser abierto con dicha herramienta
2. Si al querer abrir el archivo `preguntas_respuestas_proyecto.asta`, no posee al final *.asta* debe de agregarlo a mano, es necesario debido a que sino la herramienta no reconocera el archivo
