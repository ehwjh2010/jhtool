# -*- coding: utf-8 -*-
import typing
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, ALL_COMPLETED, Future
from dataclasses import dataclass, field
from functools import partial


@dataclass
class TaskRequest(object):
    fn: typing.Callable
    args: typing.Tuple = field(default_factory=tuple)
    kwargs: typing.Dict = field(default_factory=dict)


class ConcurrentTaskUtils(object):
    
    @classmethod
    def to_simple(cls, request_list: typing.List[TaskRequest]):
        return [partial(fn_obj.fn, *fn_obj.args, **fn_obj.kwargs) for fn_obj in request_list]
    
    @classmethod
    def concurrent_do_tasks_until_done(cls, request_list: typing.List[TaskRequest], pool: ThreadPoolExecutor = None):
        fn_list = cls.to_simple(request_list)
        if not pool:
            with ThreadPoolExecutor(max_workers=10) as executor:
                fs = [executor.submit(fn) for fn in fn_list]
                results = [r.result() for r in as_completed(fs)]
        else:
            fs = [pool.submit(fn) for fn in fn_list]
            wait(fs, return_when=ALL_COMPLETED)
            results = [f.result() for f in fs]
        return results
    
    @classmethod
    def add_tasks(cls, executor: ThreadPoolExecutor, request_list: typing.List[TaskRequest]):
        fn_list = cls.to_simple(request_list)
        fs = [executor.submit(fn) for fn in fn_list]
        return fs
    
    @classmethod
    def wait_futures_done(cls, fs: typing.List[Future], return_results: bool = False):
        wait(fs, return_when=ALL_COMPLETED)
        if return_results:
            results = [f.result() for f in fs]
            return results
