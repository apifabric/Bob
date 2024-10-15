# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Project(Base):
    """description: Table representing construction projects."""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)


class Budget(Base):
    """description: Table tracking budget allocations for projects."""
    __tablename__ = 'budgets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    amount = Column(Float, nullable=False)
    allocated_date = Column(DateTime, default=datetime.datetime.utcnow)


class Expense(Base):
    """description: Table for recording expenses against budgets."""
    __tablename__ = 'expenses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    budget_id = Column(Integer, ForeignKey('budgets.id'), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(DateTime, nullable=False)


class Contractor(Base):
    """description: Table of contractors working on projects."""
    __tablename__ = 'contractors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    contact_info = Column(String, nullable=True)


class Contract(Base):
    """description: Contracts between projects and contractors."""
    __tablename__ = 'contracts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)


class Resource(Base):
    """description: Resources used for construction projects."""
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    supplier = Column(String, nullable=True)


class ResourceAllocation(Base):
    """description: Allocation of resources to projects."""
    __tablename__ = 'resource_allocations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    resource_id = Column(Integer, ForeignKey('resources.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    allocation_date = Column(DateTime, default=datetime.datetime.utcnow)


class Employee(Base):
    """description: Employees involved in construction projects."""
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)


class EmployeeAssignment(Base):
    """description: Assignment of employees to specific projects."""
    __tablename__ = 'employee_assignments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    assignment_date = Column(DateTime, default=datetime.datetime.utcnow)


class Equipment(Base):
    """description: Equipment inventory for construction projects."""
    __tablename__ = 'equipment'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    maintainer = Column(String, nullable=True)


class EquipmentUsage(Base):
    """description: Usage records of equipment on projects."""
    __tablename__ = 'equipment_usage'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    equipment_id = Column(Integer, ForeignKey('equipment.id'), nullable=False)
    usage_hours = Column(Float, nullable=False)
    usage_date = Column(DateTime, nullable=False)


class Payment(Base):
    """description: Payments made to contractors."""
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)


# Create an SQLite database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Start a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data
sample_projects = [
    Project(name='Project Alpha', start_date=datetime.datetime(2023, 1, 15)),
    Project(name='Project Beta', start_date=datetime.datetime(2023, 2, 1)),
    # Add more sample projects
]

sample_budgets = [
    Budget(project_id=1, amount=100000.0),
    Budget(project_id=2, amount=150000.0),
    # Add more sample budgets
]

sample_expenses = [
    Expense(budget_id=1, description='Material Purchase', amount=5000.0, expense_date=datetime.datetime(2023, 1, 20)),
    Expense(budget_id=2, description='Equipment Rental', amount=7000.0, expense_date=datetime.datetime(2023, 2, 10)),
    # Add more sample expenses
]

sample_contractors = [
    Contractor(name='Smith Construction'),
    Contractor(name='Jones Builders'),
    # Add more sample contractors
]

sample_contracts = [
    Contract(project_id=1, contractor_id=1, start_date=datetime.datetime(2023, 1, 15)),
    Contract(project_id=2, contractor_id=2, start_date=datetime.datetime(2023, 2, 1)),
    # Add more sample contracts
]

sample_resources = [
    Resource(name='Cement', cost_per_unit=25.0),
    Resource(name='Steel', cost_per_unit=50.0),
    # Add more sample resources
]

sample_resource_allocations = [
    ResourceAllocation(project_id=1, resource_id=1, quantity=100.0),
    ResourceAllocation(project_id=2, resource_id=2, quantity=200.0),
    # Add more sample resource allocations
]

sample_employees = [
    Employee(name='Alice Smith', role='Architect'),
    Employee(name='Bob Brown', role='Engineer'),
    # Add more sample employees
]

sample_employee_assignments = [
    EmployeeAssignment(project_id=1, employee_id=1),
    EmployeeAssignment(project_id=2, employee_id=2),
    # Add more sample employee assignments
]

sample_equipment = [
    Equipment(name='Excavator', maintainer='Heavy Duty Co.'),
    Equipment(name='Cranes', maintainer='Lift Operations Inc.'),
    # Add more sample equipment
]

sample_equipment_usage = [
    EquipmentUsage(project_id=1, equipment_id=1, usage_hours=40.0, usage_date=datetime.datetime(2023, 1, 25)),
    EquipmentUsage(project_id=2, equipment_id=2, usage_hours=50.0, usage_date=datetime.datetime(2023, 2, 15)),
    # Add more sample equipment usage
]

sample_payments = [
    Payment(contract_id=1, amount=20000.0),
    Payment(contract_id=2, amount=25000.0),
    # Add more sample payments
]

# Add the sample data to the session
session.add_all(sample_projects)
session.add_all(sample_budgets)
session.add_all(sample_expenses)
session.add_all(sample_contractors)
session.add_all(sample_contracts)
session.add_all(sample_resources)
session.add_all(sample_resource_allocations)
session.add_all(sample_employees)
session.add_all(sample_employee_assignments)
session.add_all(sample_equipment)
session.add_all(sample_equipment_usage)
session.add_all(sample_payments)

# Commit the session to write the data into the database
session.commit()

# Close the session
session.close()
