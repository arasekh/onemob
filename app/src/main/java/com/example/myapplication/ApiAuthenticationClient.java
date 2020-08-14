package com.example.myapplication;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ApiAuthenticationClient {

    private String baseUrl;
    private String username;
    private String password;
    private String urlResource;
    private String httpMethod;
    private String urlPath;
    private String lastResponse;
    private String payload;
    private HashMap<String, String> parameters;
    private Map<String, List<String>> headerFields;

    public ApiAuthenticationClient(String baseUrl) {
        setBaseUrl(baseUrl);
    }

    private void setBaseUrl(String baseUrl) {
        this.baseUrl = baseUrl;
    }
}
