import Dashboard from "./views/Dashboard.js";
import Posts from "./views/Posts.js";

const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};


const router = async () => {
    const routes = [
        { path: "/", view: Dashboard },
        { path: "/posts", view: Posts },
        //{ path: "/posts", view: () => console.log("Viewing Post") },
        //{ path: "/settings", view: () => console.log("Viewing Settings") },
    ];

    // This will have to change.

    // Test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            isMatch: location.pathname === route.path
        };
    });


    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);
    if(!match) {
        match = {
            route: routes[0], 
            isMatch : true
        };
    }
    
    const view = new match.route.view();
    document.querySelector("#app").innerHTML = await view.getHtml();

    //console.log(match.route.view());
}; // loading each views here.

window.addEventListener("popstate", router);

document.addEventListener("DOMContentLoaded", ()=> {
    document.body.addEventListener("click", e => {
        if(e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href);
        }
        if (e.target.id === "show-image-qtm" || e.target.id === "show-image-eth") {
            const endpoint = e.target.id === "show-image-qtm" ? '/run-image-python-qtm' : '/run-image-python-eth';
            e.target.classList.add("pulsing");

            fetch(endpoint)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    const myImage = document.getElementById("my-image");
                    if (myImage && data.status === "ok") {
                        myImage.style.display = "none";
                        myImage.style.animation = '';
                        
                        myImage.src = data.imageUrl + '?' + new Date().getTime();
                        e.target.classList.remove("pulsing");
                        myImage.onload = () => {
                            myImage.style.display = "block";
                            myImage.style.opacity = "0";
                            setTimeout(() => {
                                myImage.style.animation = "fadeIn 1s forwards";
                            }, 0);
                        };
                    }
                })
                .catch(error => console.error('Error:', error));
        }
    })
    
    router();
});