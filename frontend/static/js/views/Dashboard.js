import AbstractView from "./AbstractView.js";

export default class extends AbstractView{
    constructor() {
        super();
        this.setTitle("Dashboard");
    }

    async getHtml() {
        return `
        <h1>Welcome to Gulf Crypt</h1>
        <p>Utilising the power of machine learning, get information on select coins  </p>
        <button id="show-image-qtm">
            <img src="./static/icons/qtm.png" alt="QTUM Icon" style="width: 20px; height: 20px; vertical-align: middle;"> Show QTUM Price Prediction
        </button>
        <button id="show-image-eth">
            <img src="./static/icons/eth.png" alt="ETH Icon" style="width: 20px; height: 20px; vertical-align: middle;"> Show ETH Price Prediction
        </button>
        <img id="my-image" src="./static/js/images/coin_predict.png" style="display: none;">
        `
        ;
    }
}