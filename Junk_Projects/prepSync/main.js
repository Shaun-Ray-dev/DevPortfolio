const searchForm = document.querySelector('form'); 
const searchResult = document.querySelector('.search-result'); 
const container = document.querySelector('.container'); 
let searchQuery = ''; 
const APP_ID = 'xxxxxxxx'; 
const APP_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'; 



searchForm.addEventListener('submit', async event => {
    event.preventDefault();
    searchQuery = event.target.querySelector('input').value;

    if (searchQuery) {
        try {
            searchResult.innerHTML = ''; 
            const data = await fetchAPI();
            generateHTML(data.hits);
        } 
        catch (error) {
            searchResult.innerHTML = `<p class="errorMsg">An error occurred: ${error.message}</p>`;
            console.error('Error fetching data:', error);
        }
    } else {
        searchResult.innerHTML = `<p class="errorMsg">Please enter a search query.</p>`;
    }
});



async function fetchAPI() {
    const baseURL = `https://api.edamam.com/api/recipes/v2?type=public&q=${searchQuery}&app_id=${APP_ID}&app_key=${APP_key}&to=20`;
    const response = await fetch(baseURL); 

    if (!response.ok) {
        const errorMessage = `Error ${response.status}: ${response.statusText}`;
        throw new Error(errorMessage);
    }

    return await response.json();
}



function generateHTML(results) { 
    container.classList.remove('initial'); 
    let generatedHTML = ''; 
    
    if (results.length === 0) {
        searchResult.innerHTML = `<p class="errorMsg">No recipes found. Please try a different query.</p>`;
        return;
    }
    
    results.forEach(result => { 
        generatedHTML +=
        `
                <div class="item">
                    <img src="${result.recipe.image}" alt="">
                    <div class="flex-container">
                        <h1 class="title">${result.recipe.label}</h1>
                        <a class="view-button" href="${result.recipe.url}" target="_blank">View Recipe</a>
                    </div>
                    <p class="item-data">Cuisine type: ${result.recipe.cuisineType}</p>
                    <p class="item-data">Calories: ${result.recipe.calories.toFixed(2)} g</p>
                    <p class="item-data">Diet label: ${result.recipe.dietLabels.length > 0 ? result.recipe.dietLabels : 'No Data Found'}</p>
                    <p class="item-data">Health label: ${result.recipe.healthLabels}</p>
                </div>
        `;
    });

    searchResult.innerHTML = generatedHTML;
}