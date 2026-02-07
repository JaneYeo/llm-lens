import { GoogleGenerativeAI } from "@google/generative-ai";

const API_KEY = "AIzaSyDQZyj0qPnHwzRgSN45X1bhU95YU1bztnM";

async function testModel() {
    try {
        console.log("Testing model: gemini-3-pro-preview...");
        const genAI = new GoogleGenerativeAI(API_KEY);
        const model = genAI.getGenerativeModel({ model: "gemini-3-pro-preview" });

        const result = await model.generateContent("Hello, are you there?");
        const response = await result.response;
        console.log("Success! Response:", response.text());
    } catch (error) {
        console.error("Error testing model:", error.message);
    }
}

testModel();
