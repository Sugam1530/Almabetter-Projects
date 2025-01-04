class Solution(object):
     def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums = list(set(nums))
        return len(nums)

if __name__ == "__main__":
    # nums = [0,0,1,1,1,2,2,3,3,4]
    nums = [1,1,2]
    
    solution = Solution()
    print(solution.removeDuplicates(nums))
