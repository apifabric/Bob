# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 15, 2024 19:19:31
# Database: sqlite:////tmp/tmp.Tu0CgQwKO8/Bob/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Contractor(SAFRSBaseX, Base):
    """
    description: Table of contractors working on projects.
    """
    __tablename__ = 'contractors'
    _s_collection_name = 'Contractor'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ContractList : Mapped[List["Contract"]] = relationship(back_populates="contractor")



class Employee(SAFRSBaseX, Base):
    """
    description: Employees involved in construction projects.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    EmployeeAssignmentList : Mapped[List["EmployeeAssignment"]] = relationship(back_populates="employee")



class Equipment(SAFRSBaseX, Base):
    """
    description: Equipment inventory for construction projects.
    """
    __tablename__ = 'equipment'
    _s_collection_name = 'Equipment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    maintainer = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    EquipmentUsageList : Mapped[List["EquipmentUsage"]] = relationship(back_populates="equipment")



class Project(SAFRSBaseX, Base):
    """
    description: Table representing construction projects.
    """
    __tablename__ = 'projects'
    _s_collection_name = 'Project'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    BudgetList : Mapped[List["Budget"]] = relationship(back_populates="project")
    ContractList : Mapped[List["Contract"]] = relationship(back_populates="project")
    EmployeeAssignmentList : Mapped[List["EmployeeAssignment"]] = relationship(back_populates="project")
    EquipmentUsageList : Mapped[List["EquipmentUsage"]] = relationship(back_populates="project")
    ResourceAllocationList : Mapped[List["ResourceAllocation"]] = relationship(back_populates="project")



class Resource(SAFRSBaseX, Base):
    """
    description: Resources used for construction projects.
    """
    __tablename__ = 'resources'
    _s_collection_name = 'Resource'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost_per_unit = Column(Float, nullable=False)
    supplier = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ResourceAllocationList : Mapped[List["ResourceAllocation"]] = relationship(back_populates="resource")



class Budget(SAFRSBaseX, Base):
    """
    description: Table tracking budget allocations for projects.
    """
    __tablename__ = 'budgets'
    _s_collection_name = 'Budget'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('projects.id'), nullable=False)
    amount = Column(Float, nullable=False)
    allocated_date = Column(DateTime)

    # parent relationships (access parent)
    project : Mapped["Project"] = relationship(back_populates=("BudgetList"))

    # child relationships (access children)
    ExpenseList : Mapped[List["Expense"]] = relationship(back_populates="budget")



class Contract(SAFRSBaseX, Base):
    """
    description: Contracts between projects and contractors.
    """
    __tablename__ = 'contracts'
    _s_collection_name = 'Contract'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('projects.id'), nullable=False)
    contractor_id = Column(ForeignKey('contractors.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)

    # parent relationships (access parent)
    contractor : Mapped["Contractor"] = relationship(back_populates=("ContractList"))
    project : Mapped["Project"] = relationship(back_populates=("ContractList"))

    # child relationships (access children)
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="contract")



class EmployeeAssignment(SAFRSBaseX, Base):
    """
    description: Assignment of employees to specific projects.
    """
    __tablename__ = 'employee_assignments'
    _s_collection_name = 'EmployeeAssignment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('projects.id'), nullable=False)
    employee_id = Column(ForeignKey('employees.id'), nullable=False)
    assignment_date = Column(DateTime)

    # parent relationships (access parent)
    employee : Mapped["Employee"] = relationship(back_populates=("EmployeeAssignmentList"))
    project : Mapped["Project"] = relationship(back_populates=("EmployeeAssignmentList"))

    # child relationships (access children)



class EquipmentUsage(SAFRSBaseX, Base):
    """
    description: Usage records of equipment on projects.
    """
    __tablename__ = 'equipment_usage'
    _s_collection_name = 'EquipmentUsage'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('projects.id'), nullable=False)
    equipment_id = Column(ForeignKey('equipment.id'), nullable=False)
    usage_hours = Column(Float, nullable=False)
    usage_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    equipment : Mapped["Equipment"] = relationship(back_populates=("EquipmentUsageList"))
    project : Mapped["Project"] = relationship(back_populates=("EquipmentUsageList"))

    # child relationships (access children)



class ResourceAllocation(SAFRSBaseX, Base):
    """
    description: Allocation of resources to projects.
    """
    __tablename__ = 'resource_allocations'
    _s_collection_name = 'ResourceAllocation'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('projects.id'), nullable=False)
    resource_id = Column(ForeignKey('resources.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    allocation_date = Column(DateTime)

    # parent relationships (access parent)
    project : Mapped["Project"] = relationship(back_populates=("ResourceAllocationList"))
    resource : Mapped["Resource"] = relationship(back_populates=("ResourceAllocationList"))

    # child relationships (access children)



class Expense(SAFRSBaseX, Base):
    """
    description: Table for recording expenses against budgets.
    """
    __tablename__ = 'expenses'
    _s_collection_name = 'Expense'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    budget_id = Column(ForeignKey('budgets.id'), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    expense_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    budget : Mapped["Budget"] = relationship(back_populates=("ExpenseList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    """
    description: Payments made to contractors.
    """
    __tablename__ = 'payments'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    contract_id = Column(ForeignKey('contracts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime)

    # parent relationships (access parent)
    contract : Mapped["Contract"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)
