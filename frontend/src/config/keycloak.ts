// import Keycloak from 'keycloak-js';

// let keycloakInstance: Keycloak | null = null;

// export const getKeycloakInstance = () => {
//     if (!keycloakInstance) {
//     keycloakInstance = new Keycloak({
//         url: 'http://localhost:8080',
//         realm: 'test-realm',
//         clientId: 'mafatest',
//     });
//     }
//     return keycloakInstance;
// };

// export const keycloak = getKeycloakInstance();


import Keycloak from 'keycloak-js';

let keycloakInstance: Keycloak | null = null;

export const initializeKeycloak = () => {
    if (!keycloakInstance) {
        keycloakInstance = new Keycloak({
        url: 'http://localhost:8080',
        realm: 'test-realm',
        clientId: 'mafatest',
        });
    }
    return keycloakInstance;
};

export const getKeycloak = () => {
    if (!keycloakInstance) {
        throw new Error('Keycloak не инициализирован. Сначала вызовите initializeKeycloak()');
    }
    return keycloakInstance;
};