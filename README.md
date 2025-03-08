# Instructions for Setup and Running

## Prerequisites
- Docker installed on your system
- Make utility installed

## Steps to Run

1. **Download the Data**
dowload the data on https://recipenlg.cs.put.poznan.pl/ and put it in the resources folder
the name most be 'full_dataset.csv'

1. **Build the Docker Image**
```bash
make build
```

2. **Load Recipes into Vector Database**
```bash
make load-recipes
```
> ⚠️ Note: This process may take longer them 1 hour to complete as it needs to process and index all recipes

3. **Run the Application**
```bash
make run
```

4. **Access the Application**
Open your web browser and navigate to:
```
http://localhost:8501
```

## Docs
- [Explanations](docs/EXPLANATIONS.md)
- [Examples](examples)

## Technical Stack
- Docker for containerization
- Vector database for recipe storage
- Streamlit for web interface
- Python backend

## Important Notes
- Ensure Docker daemon is running before starting
- Port 8501 must be available for the web interface
- Requires sufficient disk space for the vector database
- Internet connection needed for initial setup

## Troubleshooting
If you encounter any issues:
1. Check Docker status
2. Verify ports are not in use
3. Check system resources
4. Review logs in the terminal