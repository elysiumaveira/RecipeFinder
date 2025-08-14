import React, { createContext, useContext, useEffect, useState } from 'react';
import Keycloak from 'keycloak-js';

interface KeycloakContextType {
    keycloak: Keycloak | null;
    initialized: boolean;
}

const KeycloakContext = createContext<KeycloakContextType>({
    keycloak: null,
    initialized: false,
});

export const useKeycloakContext = () => useContext(KeycloakContext);

export const KeycloakProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [keycloak, setKeycloak] = useState<Keycloak | null>(null);
    const [initialized, setInitialized] = useState(false);

    useEffect(() => {
        const initKeycloak = async () => {
        const keycloakInstance = new Keycloak({
            url: 'http://localhost:8080',
            realm: 'test-realm',
            clientId: 'mafatest',
        });

        try {
            await keycloakInstance.init({
            onLoad: 'check-sso',
            silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
            });
            setKeycloak(keycloakInstance);
            setInitialized(true);
        } catch (error) {
            console.error('Keycloak initialization failed', error);
            setInitialized(true);
        }
        };

        if (!keycloak) {
        initKeycloak();
        }
    }, [keycloak]);

    return (
        <KeycloakContext.Provider value={{ keycloak, initialized }}>
        {children}
        </KeycloakContext.Provider>
    );
};