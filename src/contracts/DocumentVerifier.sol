// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DocumentVerifier {
    struct DocumentData {
        address issuer;
        uint256 timestamp;
        string documentName;
        string documentType;
        bool isVerified;
    }

    mapping(bytes32 => DocumentData) private documents;

    event DocumentAdded(bytes32 indexed documentHash, address indexed issuer, string documentName);
    event DocumentUpdated(bytes32 indexed documentHash, string newName, string newType);
    event DocumentDeleted(bytes32 indexed documentHash);

    /// @notice Dodaje dokument do systemu
    /// @param documentHash - hash dokumentu (SHA-256 jako bytes32)
    /// @param documentName - nazwa dokumentu
    /// @param documentType - typ dokumentu (np. pdf, certyfikat)
    function addDocument(bytes32 documentHash, string memory documentName, string memory documentType) public {
        require(documents[documentHash].issuer == address(0), "Document already exists");

        documents[documentHash] = DocumentData({
            issuer: msg.sender,
            timestamp: block.timestamp,
            documentName: documentName,
            documentType: documentType,
            isVerified: true
        });

        emit DocumentAdded(documentHash, msg.sender, documentName);
    }

    /// @notice Zwraca informacje o dokumencie
    /// @param documentHash - hash dokumentu
    /// @return isVerified - czy dokument jest zweryfikowany
    /// @return issuer - adres wydawcy
    /// @return timestamp - znacznik czasu dodania
    /// @return documentName - nazwa dokumentu
    /// @return documentType - typ dokumentu
    function verifyDocument(bytes32 documentHash)
        public
        view
        returns (
            bool isVerified,
            address issuer,
            uint256 timestamp,
            string memory documentName,
            string memory documentType
        )
    {
        DocumentData memory doc = documents[documentHash];
        return (doc.isVerified, doc.issuer, doc.timestamp, doc.documentName, doc.documentType);
    }

    /// @notice Unieważnia dokument (może to zrobić tylko wystawca)
    /// @param documentHash - hash dokumentu
    function invalidateDocument(bytes32 documentHash) public {
        require(documents[documentHash].issuer == msg.sender, "Only issuer can invalidate");
        documents[documentHash].isVerified = false;
    }

    /// @notice Aktualizuje metadane dokumentu (tylko wystawca)
    /// @param documentHash - hash dokumentu
    /// @param newName - nowa nazwa
    /// @param newType - nowy typ
    function updateDocument(bytes32 documentHash, string memory newName, string memory newType) public {
        require(documents[documentHash].issuer == msg.sender, "Only issuer can update");
        documents[documentHash].documentName = newName;
        documents[documentHash].documentType = newType;

        emit DocumentUpdated(documentHash, newName, newType);
    }

    /// @notice Usuwa dokument z rejestru (tylko wystawca)
    /// @param documentHash - hash dokumentu
    function deleteDocument(bytes32 documentHash) public {
        require(documents[documentHash].issuer == msg.sender, "Only issuer can delete");
        require(documents[documentHash].isVerified, "Document not found or already invalid");
        delete documents[documentHash];
        emit DocumentDeleted(documentHash);
    }
}
