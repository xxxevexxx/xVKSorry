import importlib
from pathlib import Path


package_path = Path(__file__).parent
module_files = [file.stem for file in package_path.glob('*.py') if file.name != '__init__.py']
__all__ = tuple(module_files)
bot_labeleres = [importlib.import_module(f'.{module}', __package__).labeler for module in module_files]
