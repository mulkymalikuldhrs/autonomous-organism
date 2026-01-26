import subprocess
import os

def create_nextjs_project(project_name: str):
    """
    Creates a new Next.js project with a simple placeholder page.

    Args:
        project_name: The name of the project.

    Returns:
        The path to the newly created project.
    """
    project_path = os.path.join("./projects", project_name)
    if os.path.exists(project_path):
        return project_path

    os.makedirs(project_path, exist_ok=True)

    # Run create-next-app
    subprocess.run(
        [
            "npx",
            "create-next-app@latest",
            project_path,
            "--ts",
            "--tailwind",
            "--eslint",
            "--app",
            "--src-dir",
            "--import-alias",
            "\"@/*\"",
            "--use-npm"
        ],
        check=True
    )

    # Overwrite the default page with a placeholder
    placeholder_page = f"""
    <div style={{ fontFamily: 'sans-serif', textAlign: 'center', marginTop: '5rem' }}>
        <h1>{project_name}</h1>
        <p>This is a placeholder for the generated SaaS product.</p>
    </div>
    """
    with open(os.path.join(project_path, "src/app/page.tsx"), "w") as f:
        f.write(placeholder_page)

    return project_path
