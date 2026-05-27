@echo off
cd /d c:\Users\ggsmo\OneDrive\Desktop\shadowtranslator
git init
git add .
git commit -m "Initial Shadow Translator upload"
git branch -M main
git remote add origin https://github.com/Shadorux/ultimate-lifeform-translator.git
git push -u origin main
pause
