folder structure:

Flask Backend
|
|___static (static folder)
|   |
|   |___css (css folder)
|       |
|       |---login.css (styling für login.html)
|       |---password_reset.css  (styling für password_reset.html)
|       |---register.css  (styling für register.html)
|       |---welcome.css (styling für hwelcome.html)
|   
|___templates (templates folder)
|   |
|   |---login.html (main structure of the Login Page)
|   |---password_reset.html (main structure of the Password Reset Page)
|   |---register.html (main structure of the Register Page)
|   |---welcome.html (main structure of the Welcome Page)
|
|---app.py (main file of the whole application)
|---read.md


App.py 
Das ist der Core von allem, wenn diese Datei nicht existieren würde, könnte man zwar die HTML-Seiten so aufrufen, 
aber der backend Server selber würde erst gar nicht gestartet und es würde auch keine Verknüpfung zu mysql hergestellt werden.
Kurz gesagt, wenn diese Datei nicht existiert, haben wir zwar einzelne Seiten, 
diese wiederum haben aber dann fast null Funktionalität.

Im Static folder storen wwir sachen wie z.B. css und js im templates folder wiederum die html dateien.