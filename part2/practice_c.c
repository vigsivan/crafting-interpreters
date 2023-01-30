#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    struct node* next;
    struct node* prev;
    int value;
} node;

typedef struct doublyLinkedList{
    node* head;
    node* tail;
    uint size;
} doublyLinkedList;

/// Insert value into an empty linked list
void insertEmpty(doublyLinkedList* dll, node* newNode){
    if (dll->size != 0){
        printf("Size is not 0, but tail is NULL");
        exit(-1);
    }

    newNode->next = NULL;
    newNode->prev = NULL;
    dll->head = newNode;
    dll->tail = newNode;
    dll->size = 1;
}

/// Append value to the list at the tail
void appendTail(doublyLinkedList* dll, int value){
    node* newNode = malloc(sizeof(node));
    newNode->value = value;
    if (dll->tail) {
        newNode->next = NULL;
        newNode->prev = dll->tail;
        dll->tail->next = newNode;
        dll->tail = newNode;
        dll->size += 1;
    }
    else {
        insertEmpty(dll, newNode);
    }
}

/// Append value to the list at the head
void appendHead(doublyLinkedList* dll, int value){
    node* newNode = (node*)malloc(sizeof(node));
    newNode->value = value;
    if (dll->head) {
        newNode->prev = NULL;
        newNode->next = dll->head;
        dll->head->prev = newNode;
        dll->head = newNode;
        dll->size += 1;
    }
    else {
        insertEmpty(dll, newNode);
    }
}

void deleteNode(doublyLinkedList* dll, node* n){
    if(n->next){
        n->next->prev = n->prev;
    }
    if(n->prev){
        n->prev->next = n->next;
    }
    if(n == dll->head){
        dll->head = n->next;
    }
    if(n == dll->tail){
        dll->tail = n->prev;
    }
    free(n);
    dll->size -= 1;
}

/// Delete first node that has given value, starting from the head
int deleteHead(doublyLinkedList* dll, int value){
    if(dll->size == 0){
        return -1;
    }
    node* ptr = dll->head;
    while(ptr && ptr->value != value){
        ptr = ptr->next; 
    }
    if(ptr){
        deleteNode(dll, ptr);
        return 0;
    }
    else{
        return -1;
    }
}

/// Delete first node that has given value, starting from the tail
int deleteTail(doublyLinkedList* dll, int value){
    if (dll->size == 0){
        return -1;
    }
    node* ptr = dll->tail;
    while(ptr && ptr->value != value){
        ptr = ptr->prev;
    }
    if(ptr){
        deleteNode(dll, ptr);
        return 0;
    }
    else {
        return -1;
    }
}


/// Search list for element, returns index if found else returns size of list
uint findHead(doublyLinkedList* dll, int value){
    node* ptr = dll->head;
    for(int i = 0; ptr; i++){
        if (ptr->value == value){
            return i;
        }
        ptr = ptr->next; 
    }
    return dll->size;
}

/// Search list for element starting from tail
uint findTail(doublyLinkedList* dll, int value){
    node* ptr = dll->tail;
    for(int i = dll->size-1; ptr; i--){
        if (ptr->value == value){
            return i;
        }
        ptr = ptr->prev; 
    }
    return dll->size;

}

doublyLinkedList* newDLL(){
    doublyLinkedList* dll = malloc(sizeof(doublyLinkedList));
    dll->head = NULL;
    dll->tail = NULL;
    dll->size = 0;
    return dll;
}

void destroyDLL(doublyLinkedList* dll){
    node* tmp = dll->head;
    while(tmp){
        node* ntmp = tmp->next;
        free(tmp);
        tmp = ntmp;
    }
    free(dll);
}

void printDLL(doublyLinkedList* dll) {
    printf("[ ");
    node* tmp = dll->head;
    while(tmp){
        printf("%d", tmp->value);
        tmp = tmp->next;
        if(tmp){
            printf(", ");
        }
    }
    printf(" ]\n");
}

int main() {
    doublyLinkedList* dll = newDLL();
    for(int i = 5; i > 0; i--){
        appendTail(dll, i*i);
    }
    deleteHead(dll, 9);
    printDLL(dll);
    for(int i = 5; i > 0; i--){
        printf("Deleting %d \n", i*i);
        if (deleteTail(dll, i*i) == 0){
            printf("Deleted %d from list, list size is now %d.\n", i*i, dll->size);
        }
        else{
            printf("Couldn't find %d in list.\n", i*i);
        }
    }
    printDLL(dll);
    for(int i = 5; i > 0; i--){
        appendTail(dll, i*i*i*i);
    }

    printDLL(dll);
    printf("4 index: %d\n", findHead(dll, 4));
    printf("%d index: %d\n", 4*4*4*4, findTail(dll, 4*4*4*4));
    destroyDLL(dll);
    return 0;
}
