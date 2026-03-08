# How to Use This Project

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your API key
4. Initialize database: `python main.py init-db`
5. Run the system: `python main.py all`
6. Open browser to `http://localhost:5000`

## Configuration

Edit `config/config.py` to:
- Add your monitoring locations
- Change monitoring interval
- Adjust detection thresholds

## Commands

- `python main.py monitor` - Run data collection only
- `python main.py dashboard` - Run dashboard only
- `python main.py all` - Run everything
- `python main.py init-db` - Initialize database