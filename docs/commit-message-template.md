# Commit Message Template

## Format Structure

```
Title of commit message

Closes #<issue number>

Description about completed tasks.
- Task 1
- Task 2
- Task 3
```

## Format Breakdown

1. **Title**: A concise, descriptive title (50-72 characters recommended)
   - Use imperative mood (e.g., "Add feature" not "Added feature")
   - Capitalize the first letter
   - No period at the end

2. **Blank Line**: Required blank line between title and body

3. **Closes Statement**: 
   - Format: `Closes #<issue number>`
   - This automatically closes the GitHub issue when merged

4. **Description**: Detailed list of completed tasks
   - Use bullet points for multiple tasks
   - Be specific about what was implemented
   - Include relevant technical details

## Example

```
Initialize Django Backend Project with PostgreSQL and DRF

Closes #2

- Created Django project structure with 'core' as project name
- Installed and configured Django 6.0 and Django REST Framework 3.16.1
- Set up PostgreSQL database configuration (psycopg2-binary)
- Configured core/settings.py with DRF in INSTALLED_APPS
- Set up basic URL routing in core/urls.py with admin interface
- Created requirements.txt with all necessary dependencies
- Added .gitignore for Python/Django artifacts
- Verified Django configuration with 'python manage.py check' (passed)
- Project structure ready for further development
```

