# Decodream Project

Decodream is a Django-based project designed to assist with interior design by leveraging AI-powered tools. It helps homeowners, designers, and architects quickly visualize and customize interior design ideas using the power of AI and 3D modeling. Whether you're looking to remodel a room, explore creative styles, or create 3D visualizations, Decodream provides an intuitive platform to bring your ideas to life.

---

## Features
- **Django Framework**: Backend powered by Django.
- **Replicate API Integration**: Uses the Replicate API for interior design image generation.
- **Style Transfer**: Allows users to apply style transfer to images.
- **Interior 3D Visualization**: Generates 3D models of interior spaces based on user input.

---

## Project Overview
The Decodream project is divided into several key components:
1. **Interior Design Generation**:
   - Users can upload an image of an interior space and use AI-powered tools to generate new interior design ideas.
   - This feature uses the Replicate API to process the uploaded image and create enhanced or remodeled designs based on user-provided prompts.
   - It allows users to visualize how their space could look with different layouts, furniture, or color schemes.

2. **Image Style Transfer**:
   - Users can apply artistic styles to interior design images, transforming them into visually appealing outputs.
   - The system uses AI to blend the selected style with the original image, creating unique and stylized versions of the interior space.
   - This feature is ideal for exploring creative design ideas or generating inspiration for interior decoration.

3. **History Page**:
   - The project includes a **History Page** where users can view previously generated designs and style transfer outputs.
   - This page allows users to:
     - Revisit past designs for reference.
     - Keep track of their design iterations and progress.
   - The history is stored securely and linked to the user's session or account.

4. **3D Visualization**:
   - The project includes functionality to generate 3D models of interior spaces based on user input.
   - Users can draw a 2D floor plan directly on the interface, which is then converted into a 3D model in real time.
   - The interface allows users to add furniture, customize layouts, and interact with the 3D model by zooming in and out or rotating the view.
   - This feature leverages the [Blueprint3D library by Furnishup](https://github.com/furnishup/blueprint3d) for rendering and managing 3D visualizations.
---

## Requirements
- Python 3.9 or higher
- Anaconda (optional, for managing environments)
- Django 4.2.3
- `python-decouple` for environment variable management
- `replicate` for API integration
- `three.js` or similar library for rendering 3D models (if applicable for frontend)

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Gwenchana10/decodreamproject.git
cd decodreamproject
```
### 2. Set Up a Virtual Environment
Using Anaconda:
```bash
conda create -n decodream_env python=3.9
conda activate decodream_env
```

Or using `venv`:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root directory (if not already present) and add the following:
```properties
DJANGO_SECRET_KEY=your_production_secret_key
DEBUG=True
REPLICATE_API_TOKEN=your_replicate_api_token
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Start the Development Server
```bash
python manage.py runserver
```

---



## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

