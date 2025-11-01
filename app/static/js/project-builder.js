// Enhanced Project Builder JavaScript - No Price Calculations
class ProjectBuilder {
    constructor() {
        this.structures = [];
        this.isCalculating = false;
        this.init();
    }

    init() {
        this.loadHouseTypeTemplates();
        this.setupEventListeners();
        
        // Ensure we start with clean state - no automatic structure
        this.clearAllStructures();
        this.cleanupStructures();
        this.updateStructuresCount();
        
        // Debug: see what structures exist
        setTimeout(() => {
            this.debugStructures();
        }, 1000);
    }

    setupEventListeners() {
        // Auto-calculate when settings change
        const houseType = document.getElementById('houseType');
        const blockType = document.getElementById('blockType');
        const wastePercentage = document.getElementById('wastePercentage');
        
        if (houseType) houseType.addEventListener('change', () => this.updateCalculation());
        if (blockType) blockType.addEventListener('change', () => this.updateCalculation());
        if (wastePercentage) wastePercentage.addEventListener('change', () => this.updateCalculation());
    }

    // Fixed addStructure method - no automatic structure
    addStructure() {
        const template = document.getElementById('structureTemplate');
        if (!template) {
            console.error('Structure template not found');
            return;
        }
        
        const clone = template.cloneNode(true);
        clone.style.display = 'block';
        clone.removeAttribute('id');
        
        const container = document.getElementById('structuresContainer');
        const emptyState = document.getElementById('emptyState');
        
        if (!container) {
            console.error('Structures container not found');
            return;
        }
        
        // Hide empty state when adding first structure
        if (emptyState && emptyState.style.display !== 'none') {
            emptyState.style.display = 'none';
        }
        
        // Show container if it's hidden
        container.style.display = 'block';
        container.appendChild(clone);
        
        // Initialize the new structure as expanded
        const newStructure = container.lastElementChild;
        const cardBody = newStructure.querySelector('.card-body');
        const toggleButton = newStructure.querySelector('.toggle-structure-btn');
        const toggleIcon = toggleButton.querySelector('i');
        
        // Start expanded
        cardBody.style.display = 'block';
        toggleIcon.className = 'bi bi-chevron-down';
        
        // Set default unit from user preferences
        const defaultUnit = document.getElementById('defaultUnit');
        if (defaultUnit) {
            newStructure.querySelector('.structure-unit').value = defaultUnit.value;
        }
        
        // Update count
        this.updateStructuresCount();
        this.updateCalculation();
    }

    // Fixed removeStructure method
    removeStructure(button) {
        const structureCard = button.closest('.structure-card');
        if (!structureCard) {
            console.error('Structure card not found');
            return;
        }
        
        structureCard.remove();
        
        // Update count and check if we should show empty state
        this.updateStructuresCount();
        this.updateCalculation();
    }
    // Temporary debug method to see all structure elements
    debugStructures() {
        console.log('=== DEBUG: All Structure Elements ===');
        
        // All structure cards in the entire document
        const allStructureCards = document.querySelectorAll('.structure-card');
        console.log('Total .structure-card elements in DOM:', allStructureCards.length);
        
        allStructureCards.forEach((card, index) => {
            const isVisible = card.offsetParent !== null;
            const parent = card.parentElement;
            const parentId = parent ? parent.id : 'no parent';
            
            console.log(`Structure ${index + 1}:`, {
                visible: isVisible,
                parent: parentId,
                text: card.querySelector('.structure-title')?.textContent,
                length: card.querySelector('.structure-length')?.value,
                width: card.querySelector('.structure-width')?.value,
                height: card.querySelector('.structure-height')?.value
            });
        });
        
        // Structure cards in container only
        const container = document.getElementById('structuresContainer');
        const containerStructures = container ? container.querySelectorAll('.structure-card') : [];
        console.log('Structures in container:', containerStructures.length);
        
        console.log('=== END DEBUG ===');
    }

    // NEW: Save project method
    async saveProject() {
        this.cleanupStructures();
        if (!this.validateProject()) {
            this.showNotification('Please fix validation errors before saving', 'error');
            return false;
        }
        
        const projectData = this.getProjectData();
        const title = document.getElementById('projectTitle').value.trim();
        const description = document.getElementById('projectDescription').value.trim();
        const houseType = document.getElementById('houseType').value;
        
        if (!title) {
            this.showNotification('Please enter a project title', 'error');
            return false;
        }
        
        if (projectData.structures.length === 0) {
            this.showNotification('Please add at least one structure', 'error');
            return false;
        }

        try {
            // Get privacy setting
            const privacyRadio = document.querySelector('input[name="privacy"]:checked');
            const privacy = privacyRadio ? privacyRadio.value : 'private';

            const response = await fetch(window.saveProjectUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title: title,
                    description: description,
                    house_type: houseType,
                    structures: projectData,
                    privacy: privacy
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showNotification('Project saved successfully!', 'success');
                
                // Redirect to view page
                setTimeout(() => {
                    window.location.href = result.redirect_url || `/project/${result.project_id}`;
                }, 1500);
                
                return true;
            } else {
                throw new Error(result.error || 'Failed to save project');
            }
        } catch (error) {
            this.showNotification('Error saving project: ' + error.message, 'error');
            return false;
        }
    }

    validateProject() {
        const structures = this.getProjectData().structures;
        
        console.log('DEBUG: Validating structures:', structures);
        
        if (structures.length === 0) {
            this.showNotification('Please add at least one structure', 'warning');
            return false;
        }

        let hasErrors = false;
        let errorMessages = [];
        
        structures.forEach((structure, index) => {
            if (structure.length <= 0 || structure.width <= 0 || structure.height <= 0) {
                const errorMsg = `Structure "${structure.name}" has invalid dimensions (${structure.length} × ${structure.width} × ${structure.height})`;
                errorMessages.push(errorMsg);
                hasErrors = true;
            }
            
            // Check for very small dimensions that might be mistakes
            if (structure.length < 1 || structure.width < 1 || structure.height < 1) {
                const warningMsg = `Structure "${structure.name}" has very small dimensions. Please double-check.`;
                console.warn(warningMsg);
            }
        });

        if (hasErrors) {
            // Show all error messages
            const errorList = errorMessages.join('\n• ');
            this.showNotification(`Please fix these issues:\n• ${errorList}`, 'error');
            return false;
        }

        this.showNotification('Project validation passed! Ready to save.', 'success');
        return true;
    }
    // Clean up any invalid/empty structures
    cleanupStructures() {
        const container = document.getElementById('structuresContainer');
        if (!container) return;
        
        const structureCards = container.querySelectorAll('.structure-card');
        let removedCount = 0;
        
        structureCards.forEach(card => {
            const length = parseFloat(card.querySelector('.structure-length').value) || 0;
            const width = parseFloat(card.querySelector('.structure-width').value) || 0;
            const height = parseFloat(card.querySelector('.structure-height').value) || 0;
            
            // Remove structures with all zero dimensions
            if (length <= 0 && width <= 0 && height <= 0) {
                card.remove();
                removedCount++;
            }
        });
        
        if (removedCount > 0) {
            console.log(`DEBUG: Cleaned up ${removedCount} invalid structures`);
            this.updateStructuresCount();
            this.updateCalculation();
        }
        
        return removedCount;
    }

    // Rest of your existing methods remain the same...
    toggleStructure(button) {
        const structureCard = button.closest('.structure-card');
        const cardBody = structureCard.querySelector('.card-body');
        const icon = button.querySelector('i');
        
        if (cardBody.style.display === 'none' || cardBody.style.display === '') {
            cardBody.style.display = 'block';
            icon.className = 'bi bi-chevron-down';
        } else {
            cardBody.style.display = 'none';
            icon.className = 'bi bi-chevron-right';
        }
    }

    addSubStructure(button) {
        const template = document.getElementById('subStructureTemplate');
        const clone = template.cloneNode(true);
        clone.style.display = 'block';
        clone.removeAttribute('id');
        
        const container = button.closest('.card-body').querySelector('.sub-structures-container');
        container.appendChild(clone);
        this.updateCalculation();
    }
    
    removeSubStructure(button) {
        button.closest('.sub-structure-card').remove();
        this.updateCalculation();
    }

    updateStructureName(select) {
        const structureCard = select.closest('.structure-card');
        const title = structureCard.querySelector('.structure-title');
        title.textContent = select.options[select.selectedIndex].text;
    }

    async updateCalculation() {
        if (this.isCalculating) return;
        
        this.isCalculating = true;
        
        // Show loading state
        const resultsContent = document.getElementById('resultsContent');
        const placeholder = document.getElementById('resultsPlaceholder');
        
        if (resultsContent) resultsContent.style.display = 'none';
        if (placeholder) {
            placeholder.style.display = 'block';
            placeholder.innerHTML = '<i class="bi bi-calculator display-4 text-muted mb-3"></i><p>Calculating blocks...</p>';
        }
        
        // Get project data
        const projectData = this.getProjectData();
        
        try {
            const response = await fetch('/api/calculate-preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ structures: projectData })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayResults(result);
            } else {
                this.showError('Calculation failed: ' + result.error);
            }
        } catch (error) {
            console.error('Calculation error:', error);
            this.showError('Network error: ' + error.message);
        }
        
        this.isCalculating = false;
    }

    getProjectData() {
        const structures = [];
        const container = document.getElementById('structuresContainer');
        
        // Only get structures from the container, not from the entire document
        const structureCards = container ? container.querySelectorAll('.structure-card') : [];
        
        structureCards.forEach(card => {
            // Only process visible structure cards (not templates)
            if (card.style.display === 'none' || card.offsetParent === null) {
                return; // Skip hidden/invisible structures
            }
            
            const length = parseFloat(card.querySelector('.structure-length').value) || 0;
            const width = parseFloat(card.querySelector('.structure-width').value) || 0;
            const height = parseFloat(card.querySelector('.structure-height').value) || 0;
            
            // Skip structures with all zero dimensions (invalid/empty structures)
            if (length <= 0 && width <= 0 && height <= 0) {
                return;
            }
            
            const structure = {
                'type': card.querySelector('.structure-type').value,
                'name': card.querySelector('.structure-title').textContent,
                'length': length,
                'width': width,
                'height': height,
                'unit': card.querySelector('.structure-unit').value,
                'sub_structures': []
            };
            
            // Get sub-structures
            const subStructureCards = card.querySelectorAll('.sub-structure-card');
            subStructureCards.forEach(subCard => {
                // Only process visible sub-structures
                if (subCard.style.display === 'none' || subCard.offsetParent === null) {
                    return;
                }
                
                const subStructure = {
                    'type': subCard.querySelector('.sub-structure-type').value,
                    'width': parseFloat(subCard.querySelector('.sub-structure-width').value) || 0,
                    'height': parseFloat(subCard.querySelector('.sub-structure-height').value) || 0,
                    'unit': subCard.querySelector('.sub-structure-unit').value,
                    'quantity': parseInt(subCard.querySelector('.sub-structure-quantity').value) || 1
                };
                structure.sub_structures.push(subStructure);
            });
            
            structures.push(structure);
        });
        
        const projectData = {
            'structures': structures,
            'block_type': document.getElementById('blockType')?.value || '9_inch_hollow',
            'waste_percentage': parseInt(document.getElementById('wastePercentage')?.value) || 10
        };
        
        console.log('DEBUG: Collected project data:', projectData);
        return projectData;
    }

    displayResults(result) {
        const resultsContent = document.getElementById('resultsContent');
        const placeholder = document.getElementById('resultsPlaceholder');
        
        if (!resultsContent || !placeholder) return;
        
        placeholder.style.display = 'none';
        resultsContent.style.display = 'block';
        
        // Safely handle all values with defaults
        const totalBlocks = result.total_blocks || 0;
        const totalArea = result.total_area || 0;
        const wastePercentage = document.getElementById('wastePercentage')?.value || 10;
        
        // Update main results
        if (document.getElementById('totalBlocks')) {
            document.getElementById('totalBlocks').textContent = totalBlocks.toLocaleString();
        }
        if (document.getElementById('netArea')) {
            document.getElementById('netArea').textContent = totalArea.toFixed(2) + ' m²';
        }
        if (document.getElementById('resultBlockType')) {
            const blockTypeSelect = document.getElementById('blockType');
            document.getElementById('resultBlockType').textContent = 
                blockTypeSelect ? blockTypeSelect.options[blockTypeSelect.selectedIndex].text : '9-inch Hollow';
        }
        if (document.getElementById('wasteAmount')) {
            document.getElementById('wasteAmount').textContent = wastePercentage + '%';
        }
        
        // Update additional materials
        if (document.getElementById('cementBags')) {
            document.getElementById('cementBags').textContent = Math.ceil((totalBlocks || 0) / 75);
        }
        if (document.getElementById('sandTrucks')) {
            document.getElementById('sandTrucks').textContent = ((totalBlocks || 0) / 2000).toFixed(1);
        }
        if (document.getElementById('laborDays')) {
            document.getElementById('laborDays').textContent = Math.ceil((totalBlocks || 0) / 80);
        }
    }

    // Fixed structure counting
    updateStructuresCount() {
        // Only count structures that are actually in the container, not templates
        const container = document.getElementById('structuresContainer');
        if (!container) return;
        
        const structures = container.querySelectorAll('.structure-card');
        const count = structures.length;
        const counter = document.getElementById('structureCounter');
        const structuresCount = document.getElementById('structuresCount');
        
        if (counter) {
            counter.textContent = `${count} structure${count !== 1 ? 's' : ''} added`;
        }
        if (structuresCount) {
            structuresCount.textContent = count;
        }
        
        const emptyState = document.getElementById('emptyState');
        
        if (count === 0) {
            if (emptyState) emptyState.style.display = 'block';
            if (container) container.style.display = 'none';
        } else {
            if (emptyState) emptyState.style.display = 'none';
            if (container) container.style.display = 'block';
        }
    }

    async autoFillStructures() {
        const houseType = document.getElementById('houseType').value;
        
        if (houseType === 'custom') {
            this.showError('Please select a specific house type for auto-fill');
            return;
        }
        
        try {
            const response = await fetch(`/api/house-type-template/${houseType}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const template = await response.json();
            
            // Clear existing structures first
            this.clearAllStructures();
            
            // Add structures from template
            if (template.structures && template.structures.length > 0) {
                for (const structureData of template.structures) {
                    await this.addStructureFromTemplate(structureData);
                    await new Promise(resolve => setTimeout(resolve, 100));
                }
                
                this.showSuccess(`Auto-filled ${template.structures.length} structures for ${template.name}!`);
            } else {
                this.showError('No structures found in template');
            }
            
            this.updateCalculation();
            
        } catch (error) {
            console.error('Auto-fill error:', error);
            this.showError('Failed to load template: ' + error.message);
        }
    }

    clearAllStructures() {
        const container = document.getElementById('structuresContainer');
        const emptyState = document.getElementById('emptyState');
        
        if (container) {
            container.innerHTML = '';
        }
        
        if (emptyState) {
            emptyState.style.display = 'block';
        }
        
        this.updateStructuresCount();
    }

    loadProjectData(projectData) {
        // Clear existing structures
        const container = document.getElementById('structuresContainer');
        const emptyState = document.getElementById('emptyState');
        
        if (container) {
            container.innerHTML = '';
        }
        
        // Set project settings
        const blockType = document.getElementById('blockType');
        const wastePercentage = document.getElementById('wastePercentage');
        
        if (blockType && projectData.block_type) {
            blockType.value = projectData.block_type;
        }
        if (wastePercentage && projectData.waste_percentage) {
            wastePercentage.value = projectData.waste_percentage;
        }
        
        // Load structures
        if (projectData.structures && projectData.structures.length > 0) {
            projectData.structures.forEach(structureData => {
                this.addStructureFromTemplate(structureData);
            });
            
            if (emptyState) emptyState.style.display = 'none';
            if (container) container.style.display = 'block';
        } else {
            if (emptyState) emptyState.style.display = 'block';
            if (container) container.style.display = 'none';
        }
        
        // Update calculation
        this.updateCalculation();
    }

    addStructureFromTemplate(structureData) {
        this.addStructure();
        
        const container = document.getElementById('structuresContainer');
        if (!container) return;
        
        const lastStructure = container.lastElementChild;
        
        // Fill structure data
        const typeSelect = lastStructure.querySelector('.structure-type');
        const lengthInput = lastStructure.querySelector('.structure-length');
        const widthInput = lastStructure.querySelector('.structure-width');
        const heightInput = lastStructure.querySelector('.structure-height');
        const unitSelect = lastStructure.querySelector('.structure-unit');
        
        // Set values
        if (typeSelect) typeSelect.value = structureData.type || 'bedroom';
        if (lengthInput) lengthInput.value = structureData.length || 0;
        if (widthInput) widthInput.value = structureData.width || 0;
        if (heightInput) heightInput.value = structureData.height || 0;
        if (unitSelect) unitSelect.value = structureData.unit || 'feet';
        
        // Update structure name
        this.updateStructureName(typeSelect);
        
        // Add sub-structures
        if (structureData.sub_structures && structureData.sub_structures.length > 0) {
            structureData.sub_structures.forEach(subData => {
                this.addSubStructureFromTemplate(lastStructure, subData);
            });
        }
    }

    addSubStructureFromTemplate(structureElement, subData) {
        const addButton = structureElement.querySelector('.btn-outline-primary');
        this.addSubStructure(addButton);
        
        const subContainer = structureElement.querySelector('.sub-structures-container');
        const lastSubStructure = subContainer.lastElementChild;
        
        // Set sub-structure values
        const typeSelect = lastSubStructure.querySelector('.sub-structure-type');
        const widthInput = lastSubStructure.querySelector('.sub-structure-width');
        const heightInput = lastSubStructure.querySelector('.sub-structure-height');
        const unitSelect = lastSubStructure.querySelector('.sub-structure-unit');
        const quantityInput = lastSubStructure.querySelector('.sub-structure-quantity');
        
        if (typeSelect) typeSelect.value = subData.type || 'door';
        if (widthInput) widthInput.value = subData.width || 0;
        if (heightInput) heightInput.value = subData.height || 0;
        if (unitSelect) unitSelect.value = subData.unit || 'feet';
        if (quantityInput) quantityInput.value = subData.quantity || 1;
    }

    resetProject() {
        if (confirm('Are you sure you want to reset the project? All structures will be removed.')) {
            const container = document.getElementById('structuresContainer');
            const emptyState = document.getElementById('emptyState');
            
            if (container) container.innerHTML = '';
            if (emptyState) emptyState.style.display = 'block';
            
            this.updateStructuresCount();
            this.updateCalculation();
        }
    }
    // Add these methods to your ProjectBuilder class in project-builder.js

    // Get structure data from a structure card element
    getStructureData(structureCard) {
        const structure = {
            'type': structureCard.querySelector('.structure-type').value,
            'name': structureCard.querySelector('.structure-title').textContent,
            'length': parseFloat(structureCard.querySelector('.structure-length').value) || 0,
            'width': parseFloat(structureCard.querySelector('.structure-width').value) || 0,
            'height': parseFloat(structureCard.querySelector('.structure-height').value) || 0,
            'unit': structureCard.querySelector('.structure-unit').value,
            'sub_structures': []
        };
        
        // Get sub-structures
        const subStructureCards = structureCard.querySelectorAll('.sub-structure-card');
        subStructureCards.forEach(subCard => {
            const subStructure = {
                'type': subCard.querySelector('.sub-structure-type').value,
                'width': parseFloat(subCard.querySelector('.sub-structure-width').value) || 0,
                'height': parseFloat(subCard.querySelector('.sub-structure-height').value) || 0,
                'unit': subCard.querySelector('.sub-structure-unit').value,
                'quantity': parseInt(subCard.querySelector('.sub-structure-quantity').value) || 1
            };
            structure.sub_structures.push(subStructure);
        });
        
        return structure;
    }

    // Set structure data to a structure card element
    setStructureData(structureCard, structureData) {
        // Set main structure values
        if (structureCard.querySelector('.structure-type')) {
            structureCard.querySelector('.structure-type').value = structureData.type || 'bedroom';
            this.updateStructureName(structureCard.querySelector('.structure-type'));
        }
        if (structureCard.querySelector('.structure-length')) {
            structureCard.querySelector('.structure-length').value = structureData.length || 0;
        }
        if (structureCard.querySelector('.structure-width')) {
            structureCard.querySelector('.structure-width').value = structureData.width || 0;
        }
        if (structureCard.querySelector('.structure-height')) {
            structureCard.querySelector('.structure-height').value = structureData.height || 0;
        }
        if (structureCard.querySelector('.structure-unit')) {
            structureCard.querySelector('.structure-unit').value = structureData.unit || 'feet';
        }
        
        // Clear existing sub-structures
        const subContainer = structureCard.querySelector('.sub-structures-container');
        if (subContainer) {
            subContainer.innerHTML = '';
        }
        
        // Add sub-structures
        if (structureData.sub_structures && structureData.sub_structures.length > 0) {
            structureData.sub_structures.forEach(subData => {
                this.addSubStructureToCard(structureCard, subData);
            });
        }
    }

    // Helper method to add sub-structure to a specific card
    addSubStructureToCard(structureCard, subData) {
        const template = document.getElementById('subStructureTemplate');
        if (!template) return;
        
        const clone = template.cloneNode(true);
        clone.style.display = 'block';
        clone.removeAttribute('id');
        
        const container = structureCard.querySelector('.sub-structures-container');
        if (!container) return;
        
        container.appendChild(clone);
        
        const lastSubStructure = container.lastElementChild;
        
        // Set sub-structure values
        const typeSelect = lastSubStructure.querySelector('.sub-structure-type');
        const widthInput = lastSubStructure.querySelector('.sub-structure-width');
        const heightInput = lastSubStructure.querySelector('.sub-structure-height');
        const unitSelect = lastSubStructure.querySelector('.sub-structure-unit');
        const quantityInput = lastSubStructure.querySelector('.sub-structure-quantity');
        
        if (typeSelect) typeSelect.value = subData.type || 'door';
        if (widthInput) widthInput.value = subData.width || 0;
        if (heightInput) heightInput.value = subData.height || 0;
        if (unitSelect) unitSelect.value = subData.unit || 'feet';
        if (quantityInput) quantityInput.value = subData.quantity || 1;
    }

    showError(message) {
        this.showNotification(message, 'danger');
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    async loadHouseTypeTemplates() {
        // Preload templates for better performance
        console.log('Loading house type templates...');
    }
}

// Initialize the project builder when the page loads
document.addEventListener('DOMContentLoaded', function() {
    window.projectBuilder = new ProjectBuilder();
});

// Global functions for HTML onclick events
function addStructure() { 
    if (window.projectBuilder) window.projectBuilder.addStructure(); 
}
function removeStructure(button) { 
    if (window.projectBuilder) window.projectBuilder.removeStructure(button); 
}
function toggleStructure(button) { 
    if (window.projectBuilder) window.projectBuilder.toggleStructure(button); 
}
function addSubStructure(button) { 
    if (window.projectBuilder) window.projectBuilder.addSubStructure(button); 
}
function removeSubStructure(button) { 
    if (window.projectBuilder) window.projectBuilder.removeSubStructure(button); 
}
function updateStructureName(select) { 
    if (window.projectBuilder) window.projectBuilder.updateStructureName(select); 
}
function updateCalculation() { 
    if (window.projectBuilder) window.projectBuilder.updateCalculation(); 
}
function autoFillStructures() { 
    if (window.projectBuilder) window.projectBuilder.autoFillStructures(); 
}
function calculateProject() { 
    if (window.projectBuilder) window.projectBuilder.updateCalculation(); 
}
function saveProject() { 
    if (window.projectBuilder) window.projectBuilder.saveProject(); 
}
function resetProject() { 
    if (window.projectBuilder) window.projectBuilder.resetProject(); 
}
function validateProject() {
    return window.projectBuilder ? window.projectBuilder.validateProject() : false;
}