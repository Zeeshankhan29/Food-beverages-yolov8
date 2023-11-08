echo [$(date)]: "Start"
echo [$(date)]: "Creating the conda virtual environment"
conda create --name checkout python=3.10 -y
echo [$(date)]: "Activating the conda virtual environment"
source  activate checkout
echo [$(date)]: "Installing the required packages"
pip install -r requirements.txt
echo [$(date)]: "End"