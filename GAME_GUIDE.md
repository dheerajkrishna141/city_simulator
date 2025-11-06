# 🏙️ City Simulation Game - Complete Guide

## 🎮 **How to Play**

### **Getting Started**

1. **Launch the Game**: Run `python main.py`
2. **Game Window**: A 1400x900 window will open with the city simulation
3. **Interface**: Left panel contains tools and information, right panel shows the city grid

---

## 🛠️ **Tools & Controls**

### **Tool Selection (Left Panel - Tools Tab)**

- **🔍 Inspect (1)**: Click on any cell to see detailed information
- **🏠 Zone (2)**: Place residential, commercial, or industrial zones
- **🏗️ Infrastructure (3)**: Build roads, power plants, water facilities
- **🏢 Building (4)**: Construct schools, hospitals, police stations, etc.
- **💥 Demolish (5)**: Remove existing structures

### **Keyboard Shortcuts**

- **1-5**: Quick tool selection
- **Space**: Pause/Resume simulation
- **Ctrl+S**: Save city
- **Ctrl+O**: Load city
- **Ctrl+N**: New city
- **Mouse Wheel**: Zoom in/out
- **Right Click + Drag**: Pan around the city

---

## 🏘️ **Zone Types**

### **Residential Zones (🏘️)**

- **Purpose**: House your city's population
- **Development**: Grows from undeveloped to high-density buildings
- **Requirements**: Power, water, road access
- **Benefits**: Provides population and tax revenue
- **Color**: Green (lighter when undeveloped)

### **Commercial Zones (🏪)**

- **Purpose**: Provide jobs and shopping
- **Development**: Grows into shopping centers and offices
- **Requirements**: Power, road access
- **Benefits**: Provides jobs and higher tax revenue
- **Color**: Blue

### **Industrial Zones (🏭)**

- **Purpose**: Manufacturing and heavy industry
- **Development**: Grows into factories and warehouses
- **Requirements**: Power, road access
- **Benefits**: Provides jobs but creates pollution
- **Color**: Brown

---

## 🏗️ **Infrastructure & Buildings**

### **Essential Infrastructure**

- **🛣️ Roads**: Connect zones and enable development
- **⚡ Power Plants**: Provide electricity (required for all zones)
- **💧 Water Facilities**: Provide water (required for residential zones)

### **Emergency Services**

- **🚒 Fire Stations**: Protect against fire disasters
- **👮 Police Stations**: Maintain law and order
- **🏥 Hospitals**: Improve health and happiness
- **🏫 Schools**: Improve education and desirability

### **Recreation & Utilities**

- **🌳 Parks**: Increase happiness and desirability
- **🗑️ Waste Facilities**: Manage pollution
- **🚇 Subway Stations**: Reduce traffic congestion

---

## 🎯 **Desirability System**

### **What is Desirability?**

Desirability is a score (0-100) that determines how attractive a zone is for development and affects its operating state.

### **Desirability Factors**

- **🏞️ Parks**: +20 points (within 10 tiles)
- **🏫 Schools**: +15 points (within 8 tiles)
- **⚡ Power Plants**: +10 points (within 12 tiles)
- **🚦 Traffic**: -2 points per traffic level
- **🛣️ Commute Distance**: -0.5 points per tile to other zones

### **Operating States**

- **Thriving (80-100)**: Bright, vibrant colors - maximum development
- **Normal (60-79)**: Standard colors - steady development
- **Struggling (30-59)**: Darker colors - slow development
- **Abandoned (0-29)**: Very dark colors - no development

---

## 🚨 **Disaster System**

### **Types of Disasters**

- **🔥 Fire**: Damages buildings within radius, severity 1-3
- **🌪️ Tornado**: Large area damage, severity 1-3

### **Disaster Management**

- **Fire Stations**: Protect against fires (8-tile radius)
- **Police Stations**: Maintain order during disasters
- **Disaster Risk**: Affects zone desirability
- **Recovery**: Disasters last 3-9 days based on severity

### **Disaster Effects**

- Damage to infrastructure and buildings
- Reduced desirability in affected areas
- Economic impact on the city
- Visual warnings on the map

---

## 🚦 **Traffic System**

### **How Traffic Works**

- **Daily Calculation**: Traffic is calculated every day based on commutes
- **Commute Paths**: Traffic follows the shortest road path between zones
- **Traffic Levels**:
  - **Low (Yellow)**: 1-3 vehicles
  - **Medium (Orange)**: 4-6 vehicles
  - **High (Red)**: 7+ vehicles

### **Traffic Effects**

- **Desirability Penalty**: High traffic reduces zone desirability
- **Visual Indicators**: Traffic levels shown on roads
- **Economic Impact**: Affects zone development and tax revenue

### **Traffic Management**

- **Road Network**: Expand road network to distribute traffic
- **Subway Stations**: Reduce road traffic
- **Zone Planning**: Separate residential and industrial areas

---

## 📊 **City Management**

### **Key Statistics**

- **💰 Money**: Your city's budget
- **👥 Population**: Total residents
- **😊 Happiness**: Overall citizen satisfaction (0-100%)
- **💼 Employment Rate**: Percentage of working population
- **🌫️ Pollution**: Environmental pollution level
- **💵 Tax Revenue**: Monthly income from taxes
- **🔧 Maintenance Cost**: Monthly infrastructure costs

### **Economic Balance**

- **Income**: Tax revenue from zones and buildings
- **Expenses**: Infrastructure maintenance and emergency services
- **Budget Management**: Balance growth with financial stability

---

## 🎯 **Strategy Guide**

### **Early Game (First 30 Days)**

1. **Start Small**: Begin with a few residential zones
2. **Essential Infrastructure**: Build roads, power plant, water facility
3. **Basic Services**: Add a fire station and police station
4. **Monitor Finances**: Keep maintenance costs low

### **Mid Game (30-100 Days)**

1. **Expand Zones**: Add commercial and industrial zones
2. **Improve Desirability**: Build parks and schools
3. **Emergency Services**: Ensure good coverage
4. **Traffic Management**: Monitor and manage traffic flow

### **Late Game (100+ Days)**

1. **Optimize Layout**: Maximize desirability scores
2. **Disaster Preparedness**: Strong emergency service coverage
3. **Economic Growth**: Balance all zone types
4. **City Planning**: Create efficient road networks

### **Pro Tips**

- **Zone Placement**: Place residential zones near parks and schools
- **Industrial Zones**: Keep them away from residential areas
- **Road Planning**: Create efficient road networks to reduce traffic
- **Emergency Services**: Ensure good coverage across the city
- **Desirability**: Monitor the Desirability tab to optimize zone placement
- **Disaster Response**: Build fire stations and police stations strategically

---

## 🏆 **Victory Conditions**

### **Success Metrics**

- **Population**: 10,000+ residents
- **Happiness**: 80%+ citizen satisfaction
- **Employment Rate**: 90%+ employment
- **Financial Stability**: Positive monthly income
- **Low Pollution**: Under 30% pollution level

### **Advanced Goals**

- **Thriving Zones**: All zones in "thriving" state
- **Disaster Resilience**: No damage from disasters
- **Traffic Efficiency**: Low traffic congestion
- **Economic Growth**: High tax revenue

---

## 🔧 **Troubleshooting**

### **Common Issues**

- **Zones Not Developing**: Check power, water, and road access
- **Low Desirability**: Add parks, schools, and reduce traffic
- **Financial Problems**: Reduce maintenance costs or increase tax revenue
- **Disaster Damage**: Build more emergency services
- **High Traffic**: Expand road network or add subway stations

### **Performance Tips**

- **Save Regularly**: Use Ctrl+S to save your progress
- **Monitor Statistics**: Check the Statistics tab frequently
- **Plan Ahead**: Think about future expansion when placing zones
- **Balance Growth**: Don't expand too quickly

---

## 🎮 **Advanced Features**

### **Simulation Controls**

- **Speed Control**: Adjust simulation speed (0.5x to 5x)
- **Manual Advancement**: Advance time manually
- **Pause/Resume**: Control simulation flow

### **File Management**

- **Save/Load**: Save your city and load previous saves
- **Quick Save**: Use the quick save feature for convenience
- **New City**: Start fresh when needed

---

## 🎯 **Final Tips**

1. **Start Small**: Don't try to build everything at once
2. **Monitor Desirability**: Use the Desirability tab to optimize placement
3. **Plan for Disasters**: Build emergency services early
4. **Manage Traffic**: Watch for traffic congestion and plan accordingly
5. **Balance Growth**: Maintain a healthy mix of zone types
6. **Save Often**: Protect your progress with regular saves
7. **Experiment**: Try different layouts and strategies
8. **Have Fun**: Enjoy building and managing your virtual city!

---

**Good luck, Mayor! 🏙️✨**
