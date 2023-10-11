# Optimal Delivery Schema Generator

## Description

Optimal Delivery Schema Generator is a simple tool to generate a delivery schema for a given set of destinations and vehicles. It uses a random restart hill climb approach to find the optima solution. The project is written in Python. This project is developed as a solution for an Assignment of the course CS3613 - Introduction to Artificial Intelligence at Department of Computer Science and Engineering, University of Moratuwa, Sri Lanka.

input.txt file includes the map and the details about trucks. The first n lines of this file contain the city map as n x n matrix (elements in the rows are separated by comma), where n is the number of delivery locations + courier service station. Each cell value of the matrix represents the distance between the nodes. “N” means there is no road between the nodes. n+1 line onwards, you are given the information about the trucks that belong to the courier service in the format
“truck\_<<number>>#<<capacity>>”.

## Usage

1. Clone the repository

```bash
git clone https://github.com/sajitha-tj/optimal-delivery-schema-generator.git
```

2. Navigate to the project directory

```bash
cd optimal-delivery-schema-generator
```

3. Change the input file as required

4. Run the program

```bash
python main.py
```

## Output

The output will be printed in the console and will be saved in the output.txt file.

## Appendix

### Input File Format

```txt
0,5,N,N,N,6
5,0,19,N,15,N
N,19,0,22,N,10
N,N,22,0,10,N
N,15,N,10,0,12
6,N,10,N,12,0
truck_1#2
truck_2#3
```
