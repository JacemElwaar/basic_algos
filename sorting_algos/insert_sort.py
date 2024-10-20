

def insert_increasing_sort_algo(A , n,  start_index = 1): 
    for i in range(start_index,n): 
        key = A[i]
        j = i-1 
        while A[j]>key and j>=start_index-1: 
            A[j+1] = A[j]
            j-=1
        A[j+1] = key        
    return A
 


def insert_decresing_sort_algo(A, n, start_index=1): 
    for i in range(start_index,n):
        key = A[i]
        j = i-1 
        while key>A[j] and j>=start_index-1: 
            A[j+1] = A[j]
            j-=1
        A[j+1]= key
    return A


def central_sort_slgo(A,n, param):
    if param:  
        A = insert_decresing_sort_algo(A ,int(n/2), 1)
        A = insert_increasing_sort_algo(A ,n, int(n/2)+1)
    else : 
        A = insert_increasing_sort_algo(A ,int(n/2), 1)
        A = insert_decresing_sort_algo(A ,n, int(n/2)+1)
    
    return A


def verify_sorting(A, n, start_index=1, param=0): 
    j = start_index
    if param: 
        while j+1<n: 
            if A[j] > A[j+1]:
                return False
            j+=1
    else: 
        while j+1<n: 
            if A[j] < A[j+1]:
                return False
            j+=1
    return True





if __name__ == "__main__":

    Input_list = [1,2,3,4,5,1,2,3,4,5,0,0]    
    n = len(Input_list)
    print("sort increasingly", insert_increasing_sort_algo(Input_list,n))
    print("verify sort", verify_sorting(Input_list,n,1,1))
    print()
    
    Input_list = [1,2,3,4,5,1,2,3,4,5,0,0]
    print("sort decreasingly", insert_decresing_sort_algo(Input_list,n))
    print("verify sort", verify_sorting(Input_list,n,1,0))
    print()

    Input_list = [1,2,3,4,5,1,2,3,4,5,0,0]
    print("inside central sort", central_sort_slgo(Input_list,n,1))
    print("verify sort", bool(verify_sorting(Input_list,int(n/2),1,0) and verify_sorting(Input_list,n,int(n/2)+1,1)))
    print()
    
    Input_list = [1,2,3,4,5,1,2,3,4,5,0,0]
    print("outside central sort", central_sort_slgo(Input_list,n,0))
    print("verify sort", bool(verify_sorting(Input_list,int(n/2),1,1) and verify_sorting(Input_list,n,int(n/2)+1,0)))