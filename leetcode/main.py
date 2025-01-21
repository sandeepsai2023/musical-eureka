from typing import List

# # class Solution:
# #     def merge(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
# #         nums1[m:]=nums2
# #         print(nums1)
# #         """
# #         Do not return anything, modify nums1 in-place instead.
# #         """
        

# # temp = Solution()
# # temp.merge(nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3)
# # # nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3

# class Solution:
#     def maxScoreSightseeingPair(self, values: List[int]) -> int:
#         max_val = 0
#         max_i = 0
#         i=0
#         j=i+1
#         # for i in range(0,len(values)):
#         while i<len(values):
#             # for j in range(i+1,len(values)):
#             max_i = values[i]+i
#             # temp = (values[i] + values[j]) - (j - i)
#             # values_2.append(temp)
#             if max_val<temp:
#                 max_val=temp
#             else:
#                 pass
#             j = i+1
#         return max_val
    

# print(Solution().maxScoreSightseeingPair(values = [8,1,5,2,6]))


class Solution:
    def maxScoreSightseeingPair(self, values: List[int]) -> int:
        # max_val = 0
        # max_i = 0
        # i=0
        # j=i+1
        # for i in range(0,len(values)):
        # # while i<len(values):
        #     for j in range(i+1,len(values)):
        #         temp = (values[i] + values[j]) - (j - i)
        #         # values_2.append(temp)
        #         if max_val<temp:
        #             max_val=temp
        #         else:
        #             pass
        #         j = i+1
        # return max_val

        max_i = 0
        max_val = 0
        for j in range(1,len(values)):
            i=j-1
            temp_i = values[i]+i
            if max_i<temp_i:
                max_i = temp_i
            
            temp_value = max_i+values[j]-j
            # if j==1:
            #     max_val = temp_value
            # else:
            #     temp_value = max_i+values[j]-j
            
            if max_val<temp_value:
                max_val = temp_value
                # max_val = max_i+temp_value

            # print(i,max_i,temp_value,max_val)
        return max_val
    
    # def mincostTickets(self, days: List[int], costs: List[int]) -> int:


    def stringMatching(self, words: List[str]) -> List[str]:
        substr = list()
        for i in range(0,len(words)):
            print(i)
            for j in range(i+1,len(words)):
                print(j)
                if (words[i] in words[j]):
                    substr.append(words[i])
                elif (words[j] in words[i]):
                    substr.append(words[j])
                else:
                    continue
        
        return list(set(substr))


    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        # for i in words1:
        #     ls = [i.contains(j) for j in ]
        return 0
        
# print(Solution().stringMatching(words = ["mass","as","hero","superhero"]))