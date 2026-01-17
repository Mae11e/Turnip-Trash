#!/usr/bin/env python3
"""
Script de lancement pour Turnip Trash
Usage:
    python launch.py           # Lance le jeu normalement
    python launch.py --web     # Build et lance le serveur web
    python launch.py --build   # Build pour le web sans lancer
"""
import sys
import os
import subprocess
import argparse

def run_game():
    """Lance le jeu normalement."""
    print("🎮 Lancement du jeu en mode local...")
    venv_python = os.path.join("template", "venv", "bin", "python3")

    if os.path.exists(venv_python):
        subprocess.run([venv_python, "game/main.py"])
    else:
        print("⚠️  Environnement virtuel non trouvé, utilisation de python3 système")
        subprocess.run(["python3", "game/main.py"])

def build_web():
    """Build le jeu pour le web avec pygbag."""
    print("🔨 Build du jeu pour le web avec pygbag...")

    # Vérifie si build_env existe
    build_env_python = os.path.join("build_env", "bin", "python3")

    if not os.path.exists(build_env_python):
        print("📦 Installation de pygbag...")
        subprocess.run(["python3", "-m", "venv", "build_env"])
        subprocess.run([build_env_python, "-m", "pip", "install", "pygbag"])

    # Build avec pygbag
    print("🏗️  Building...")
    subprocess.run([build_env_python, "-m", "pygbag", "--build", "game"])

    # Créer le ZIP
    print("📦 Création du ZIP...")
    os.chdir("game/build")
    subprocess.run(["zip", "-r", "../../turnip-trash-web.zip", "web/"])
    os.chdir("../..")

    print("✅ Build terminé!")
    print(f"📁 Fichier: turnip-trash-web.zip")

def run_web_server():
    """Lance le serveur web pour tester le build."""
    web_dir = os.path.join("game", "build", "web")

    if not os.path.exists(web_dir):
        print("⚠️  Build web non trouvé. Lancement du build...")
        build_web()

    print("🌐 Lancement du serveur web local...")
    print("📡 Serveur disponible sur: http://localhost:8000")
    print("⚠️  Note: La page peut être noire en local (limitation CORS)")
    print("   Pour tester complètement, upload sur itch.io!")
    print("\n🛑 Appuyez sur Ctrl+C pour arrêter le serveur\n")

    os.chdir(web_dir)
    try:
        subprocess.run(["python3", "-m", "http.server", "8000"])
    except KeyboardInterrupt:
        print("\n\n👋 Serveur arrêté!")

def main():
    parser = argparse.ArgumentParser(
        description="Lance Turnip Trash en mode jeu ou web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python launch.py           Lance le jeu normalement
  python launch.py --web     Build et lance le serveur web
  python launch.py --build   Build seulement (pour upload itch.io)
        """
    )

    parser.add_argument(
        "--web",
        action="store_true",
        help="Build et lance le serveur web local"
    )

    parser.add_argument(
        "--build",
        action="store_true",
        help="Build pour le web sans lancer le serveur"
    )

    args = parser.parse_args()

    # Change vers le répertoire du script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    if args.build:
        build_web()
    elif args.web:
        run_web_server()
    else:
        run_game()

if __name__ == "__main__":
    main()
