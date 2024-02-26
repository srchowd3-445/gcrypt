import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor() {
        super();
        this.setTitle("About Us");
    }

    async getHtml() {
        return `
        <h1>About Us</h1>
        <p>MENA Based Media Platform bringing you the latest unbiased news & guides for the Blockchain & Crypto-currency ecosystem.</p>
        `
        ;
    }
}