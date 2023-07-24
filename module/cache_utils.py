import cachetools.func

class CacheManager():

    def __init__(self, key_name : str ) -> None:
        # print("cache manager")
        self.cache_list = []
        self.key_name = key_name

    # @cachetools.func.ttl_cache(maxsize=1000*1024, ttl= 60 * 60)
    def get_cache(self, key ) -> dict :
        for cache in self.cache_list:
            if cache[ self.key_name ] == key:
                print("[CACHE] found cache!!! ")
                return cache

        print("[CACHE] NOT found cache!!! ")
        return None


    def set_cache(self, data : dict ) -> None:
        self.cache_list.append( data )
