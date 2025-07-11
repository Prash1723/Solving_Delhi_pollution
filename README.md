# Solving Delhi pollution

The aim of the project is to largely identify the pollution levels in the second most populated city in the world and ideally come up with a solution. Initially, for visualization we have a Dashboard to view all the statistics in the problem. A machine learning model to predict the future of the city.

## Dataset

The dataset used is the air pollution records for 2015-2023 and it features the pollutant levels, the type and safety level of each day.

## Requirements

- Python 3.12.3
- IDE
- Internet (For Dashboard)
- Modules:
    - Pandas
    - Numpy
    - Bokeh
    - Scikit-learn

## Run

To run this project, follow the steps:

1. Clone the repository:

```bash
git clone https://github.com/Prash1723/Solving_Delhi_pollution.git
```

2. Navigate to the project folder:

```bash
cd Solving_Delhi_pollution
```

3. Install the required modules

```bash
pip3 install -r requirements.txt
```

4. Run the python file (Dashboard)

```bash
bokeh serve --show script.py
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.

## Acknowledgments

The analysis is inspired by the author's desire to identify, track and try to find a solution to the impending problem with the air quality in the city.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Conclusion

In the analysis, we see that most prominent pollutants affecting the overall air quality is PM2.5 and PM10 particulate matters, particularly in the winter. 
