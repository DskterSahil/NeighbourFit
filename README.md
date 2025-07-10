# NeighborFit Delhi: A Lifestyle-Based Neighborhood Matching Engine

**"A home is not just a structure or a financial investment; it is a platform upon which a life is built."**

🔗 **Live App**: (https://neighbourfitbysahil.netlify.app/)

-----

## 📌 Project Brief

**NeighborFit** is a full-stack web application meticulously designed to address the challenges individuals face when relocating to Delhi and finding a neighborhood that genuinely aligns with their lifestyle. It employs a sophisticated, data-driven approach, integrating a custom data processing pipeline, a weighted-average matching algorithm, and an intuitive user interface to deliver personalized neighborhood recommendations.

-----

## 1\. Problem Analysis & Research

### 1.1 Problem Definition and Hypothesis Formation

Relocating to a vast and diverse metropolis like Delhi presents significant hurdles in identifying neighborhoods that resonate with individual lifestyle priorities. Traditional real estate platforms primarily focus on property listings, often lacking the personalized, data-driven tools necessary to rank localities based on a holistic set of factors such as commute times, community feel, family needs, or student-specific amenities. NeighborFit aims to bridge this critical gap.

**Hypotheses:**

  * **Proxy Metric Validity:** We hypothesize that abstract user needs, such as a desire for a "Community Feel" or a specific "Vibe," can be effectively represented by **proxy scores**. These scores are derived from quantifiable data like the density of parks, local markets, and community centers, enabling us to translate subjective preferences into measurable metrics.
  * **Persona-Based Matching:** We believe that a **weighted-average algorithm** can produce meaningful and differentiated rankings that align with intuitive user personas. For instance, a user prioritizing "Family Friendly" factors will receive distinctly different neighborhood recommendations compared to a user whose primary concern is "Study & Coaching" facilities.
  * **User-Centric Value:** We theorize that a tool empowering users to actively weigh their own priorities will be perceived as significantly more valuable than static lists of "top 10" neighborhoods, offering a truly personalized experience.

### 1.2 Research Methodology and Findings Analysis

**Methodology:** To quickly gather insights within the project's time constraints, we conducted rapid user research. This involved analyzing discussions on popular online forums, specifically Reddit's `r/delhi`, and reviewing the features and user experiences of existing real estate portals like 99acres and MagicBricks. This qualitative research was crucial in identifying common user pain points and understanding the priorities that ultimately contribute to a resident's quality of life and satisfaction within a neighborhood.

**Findings & Gaps:** Our analysis revealed a significant disparity: existing solutions excel at providing property-specific data (e.g., price, size) but fall short in offering quantifiable, neighborhood-level lifestyle insights. There was a clear and unmet need for a tool that could answer subjective yet critical questions like "Which area is best for a student?" or "Where is it quiet and family-friendly?" This observation directly led to our core decision: to develop **proxy metrics** to effectively fill these crucial data gaps and provide comprehensive neighborhood insights.

-----

## 2\. Technical Implementation

### 2.1 System Architecture

The NeighborFit application is built upon a robust, three-tiered system architecture, designed for efficiency, scalability, and user responsiveness:

  * **Data Processing Pipeline (Python):** A standalone Python script, `data_processing/data_processor.py`, forms the backbone of our data intelligence. It's responsible for offline data collection, fetching raw amenity counts from the **Foursquare Places API**, calculating distances to metro stations using the `geopy` library, normalizing the collected data, creating composite scores for various lifestyle factors, and finally, outputting a single, clean `processed_delhi_data.json` file. This offline approach is crucial for ensuring rapid API response times during live use and for staying within the free-tier limits of the external APIs.
  * **Backend API (Node.js & Express):** A lightweight and efficient Express server, `backend/server.js`, serves as the application's brain. Upon startup, it loads the comprehensive `processed_delhi_data.json` file into memory, enabling extremely fast data retrieval. It exposes a single, highly optimized `/match` endpoint. This endpoint receives user preferences from the frontend, applies our sophisticated matching algorithm in real-time, and returns a precisely sorted list of recommended neighborhoods.
  * **Frontend (React):** The user interface, built with React (`frontend/neighbourfit/`), provides a highly responsive and intuitive experience. Users can easily input their lifestyle preferences using a series of interactive sliders. The frontend communicates seamlessly with the backend via an `axios` POST request, dynamically displaying the ranked neighborhood results in a clear and engaging manner.

### 2.2 Algorithm Design Rationale and Trade-offs

**Algorithm:** The core of NeighborFit's recommendation engine is a **weighted-average matching algorithm**. This algorithm operates in several key steps:

1.  All raw data points (e.g., amenity counts, distances) are first **normalized to a common 0-1 scale** using min-max scaling, ensuring that different metrics contribute equally to the overall score.
2.  For metrics where "less is better" (e.g., distance to metro), the scores are **inverted** so that lower values yield higher normalized scores.
3.  Each neighborhood's normalized score for a given factor is then multiplied by the **user's stated preference (weight)** for that factor.
4.  The **final score** for each neighborhood is the sum of these weighted scores, normalized by the total weight applied by the user.

**Rationale:** This model was deliberately chosen for its **transparency**, **ease of implementation**, and **direct testability**. It provides a clear, understandable, and logical link between user input and the final neighborhood recommendations, making the results easily interpretable for the user.

**Trade-offs:**

  * The primary trade-off in our algorithm design was between **simplicity and complexity**. While a more sophisticated model (e.g., a machine learning-based approach) might potentially offer more nuanced results, it would demand significantly more data for training and substantially greater development time. Our approach prioritizes a functional, explainable, and readily deployable system over potential marginal gains in nuance.
  * Another key trade-off involved the **use of proxy data**. Relying on proxies to evaluate abstract concepts like "community feel" or "vibe" is a practical and necessary solution to the challenge of data scarcity for such qualitative attributes. However, it's inherently less precise than direct measurement, acknowledging that these proxies provide a good approximation rather than an exact representation.

### 2.3 Data Challenges Encountered and Solutions Implemented

Building NeighborFit involved navigating several data-related complexities. Here's how we addressed them:

  * **Challenge 1: Lack of Official Boundary Data:** Official GeoJSON files, which precisely delineate Delhi neighborhood boundaries, are not readily available in public datasets. This posed a significant hurdle for accurately associating amenities and distances with specific localities.
      * **Solution:** We addressed this by approximating neighborhoods as a **circular radius** (e.g., 1.5km) around a manually defined central coordinate for each area. While a simplification, this proved to be a practical and effective method to make the data collection and association feasible within the project's scope.
  * **Challenge 2: Measuring Abstract Concepts:** Quantifying qualitative concepts like "Community Feel" or "Family Friendliness" solely with raw data is inherently difficult. These subjective aspects are crucial for lifestyle matching but lack direct numerical representation.
      * **Solution:** We engineered **proxy metrics**. For example, "Family Friendly" was defined as a **composite score** derived from the counts of schools, playgrounds, and daycares within a neighborhood's defined radius. This innovative approach effectively translates abstract user needs into measurable, data-driven factors, allowing the algorithm to account for these subjective preferences.

-----

## 3\. Testing & Validation

### 3.1 Testing Approach

To ensure the logical consistency and real-world applicability of our algorithm, the application was rigorously tested using a **persona-based approach**. We simulated various user profiles by systematically adjusting the input sliders to extreme values, mirroring distinct lifestyle priorities.

### 3.2 Validation Results

The persona-based testing yielded highly encouraging results, validating the algorithm's effectiveness:

  * **Persona 1: The Student:** When the "Study & Coaching" and "Metro Proximity" sliders were set to maximum, and "Family Friendly" to minimum, the model successfully recommended neighborhoods widely known to be student hubs in Delhi, such as **Greater Kailash**. This demonstrated the algorithm's ability to prioritize academic and connectivity needs.
  * **Persona 2: The Family:** Conversely, when the "Family Friendly" and "Community Feel" sliders were set to maximum, the model accurately recommended greener, more residential areas characterized by a higher concentration of parks and schools, such as **Green Park**. This validated its capacity to identify family-oriented environments.

**Conclusion:** The consistency of these persona-based test results confirms that the algorithm and its underlying proxy metrics are logically sound and produce intuitive, real-world relevant neighborhood recommendations.

-----

## 4\. Analysis & Reflection

### 4.1 Critical Evaluation of Solution's Effectiveness

**Strengths:** NeighborFit proves highly effective as a **first-order filter**. It successfully transforms the overwhelming task of choosing from Delhi's myriad neighborhoods into a manageable list of data-backed suggestions. This empowers users to embark on their detailed property search with significantly increased confidence and a more focused direction. The application's strength lies in its ability to translate subjective lifestyle preferences into actionable, data-driven recommendations.

**Weaknesses:** The model's accuracy is inherently limited by its reliance on **proxies**. It cannot fully capture the nuanced "vibe," ambient noise levels, or the perceived safety of a neighborhood, which are often highly qualitative attributes. Furthermore, the accuracy and completeness of the underlying data are subject to the quality and updates of the **Foursquare API**, which is our primary data source.

### 4.2 Identified Limitations and Future Improvements

Based on our analysis, we've identified several key limitations and corresponding avenues for future enhancement:

  * 
<!-- end list -->

```
-----

**Limitation 1: Static Data & Cold Starts:** The current data used by the application is a **static snapshot**, meaning it doesn't automatically update over time. Additionally, the free-tier backend hosting solution experiences "cold starts" – a delay of 30-60 seconds for the first user after 15 minutes of inactivity, as the server needs to spin up.

  * **Improvement:** A significant future improvement would involve implementing a **scheduled cron job** to periodically run the Python data processing pipeline, ensuring the data remains fresh and up-to-date. Migrating the backend to a **paid hosting tier** would effectively eliminate cold start delays, providing a consistently fast user experience.
```

  * 
<!-- end list -->

```
-----

**Limitation 2: Simple Proxies:** Our current proxy metrics, while effective, are based on relatively simple counts of amenities.

  * **Improvement:** Future iterations could incorporate a much richer array of data layers to create more nuanced and accurate scores. This could include integrating **air quality data**, **real-time traffic patterns**, and perhaps even **user-submitted reviews or sentiment analysis** from local forums to capture a more holistic picture of a neighborhood's characteristics.
```

  * 
<!-- end list -->

```
-----

**Limitation 3: Scalability:** The current data model involves loading a single, relatively large JSON file into memory, which is efficient for a single city like Delhi but would not be scalable for supporting multiple cities or vastly larger datasets.

  * **Improvement:** To ensure future scalability and support for a broader geographic scope, a crucial improvement would be to migrate the data to a robust **relational database**, such as **PostgreSQL, with the PostGIS extension**. PostGIS provides powerful capabilities for geographic queries and spatial indexing, making it ideal for managing and querying large datasets of neighborhood information across multiple cities.
```

-----

## 💻 Tech Stack

  * **Frontend:** React, Axios, CSS (Dark Theme)
  * **Backend:** Node.js, Express
  * **Data Processing:** Python, Pandas, Geopy
  * **APIs Used:** Foursquare Places API

-----

## 📂 Folder Structure

```
NeighbourFit/
├── backend/
│   ├── server.js
│   └── processed_delhi_data.json
├── data-processing/
│   ├── data_processing.py
│   ├── delhi_neighborhoods.csv
│   └── metro_stations.csv
├── frontend/
│   └── neighbourfit/
│       └── src/
│           ├── App.jsx
│           └── App.css
```

-----

## 🚀 How to Run Locally

To get NeighborFit up and running on your local machine, follow these simple steps:

```bash
# Backend
cd backend
npm install
node server.js

# Frontend
cd frontend/neighbourfit
npm install
npm run dev
```

-----

## 📢 Contact

**Created by Sahil Prajapati**

  * GitHub: [DskterSahil](https://github.com/DskterSahil)
  * LinkedIn: [linkedin.com/in/dsktersahil](https://linkedin.com/in/dsktersahil)